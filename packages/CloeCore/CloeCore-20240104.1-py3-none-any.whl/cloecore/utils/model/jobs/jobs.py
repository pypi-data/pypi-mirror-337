from __future__ import annotations

import json
import logging
import pathlib
import uuid
from typing import ClassVar, Type

from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators
from cloecore.utils.model.jobs import DB2FS, FS2DB, ExecSQL

logger = logging.getLogger(__name__)


class Jobs(BaseModel):
    """Base class for loading CLOE Job model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("jobs")

    jobs: list[DB2FS | FS2DB | ExecSQL] = Field(default=[], exclude=True)
    jobs_cache: dict[uuid.UUID, DB2FS | FS2DB | ExecSQL] = Field(
        default={}, exclude=True
    )

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("jobs")
    def child_uniqueness_check(cls, value: list[DB2FS | FS2DB | ExecSQL]):
        validators.find_non_unique(value, "name")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[Jobs, list[ValidationError | json.JSONDecodeError]]:
        instances: list[DB2FS | FS2DB | ExecSQL] = []
        errors = []
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances_path = input_path / cls.subfolder_path
        sub_jobs: list[Type[DB2FS] | Type[FS2DB] | Type[ExecSQL]] = [
            DB2FS,
            FS2DB,
            ExecSQL,
        ]
        for sub_job in sub_jobs:
            sub_instances, sub_errors = sub_job.read_instances_from_disk(
                instances_path / sub_job.__name__.lower()
            )
            instances += sub_instances
            errors += sub_errors
        try:
            instance = cls(jobs=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.jobs:
            child.write_to_disk(
                output_path / self.subfolder_path / child.__class__.__name__.lower()
            )

    def get_job_by_id(self, jobs_id: uuid.UUID) -> DB2FS | FS2DB | ExecSQL:
        if len(self.jobs_cache) < 1:
            self.jobs_cache = {jobs.id: jobs for jobs in self.jobs}
        return self.jobs_cache[jobs_id]

    def get_jobs_of_type(
        self,
        job_type: Type[DB2FS] | Type[FS2DB] | Type[ExecSQL],
    ) -> list[DB2FS | FS2DB | ExecSQL]:
        """
        Filters the jobs list based on the given job type.

        :param job_type: Type of the job
        :return: List of jobs of the specified type
        """
        return [job for job in self.jobs if isinstance(job, job_type)]

    def check_if_job_exists_by_id(self, jobs_id: uuid.UUID) -> bool:
        if len(self.jobs_cache) < 1:
            self.jobs_cache = {job.id: job for job in self.jobs}
        return jobs_id in self.jobs_cache

    def get_exec_sql_jobs(
        self,
    ) -> list[ExecSQL]:
        """
        Filters the jobs list

        :return: List of jobs of the specified type
        """
        return [job for job in self.jobs if isinstance(job, ExecSQL)]
