import logging
import uuid
from typing import Type

from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators
from cloecore.utils.model.jobs import DB2FS, FS2DB, exec_sql

logger = logging.getLogger(__name__)


class Jobs(BaseModel):
    """Base class for loading CLOE Job model objects."""

    jobs: list[DB2FS | FS2DB | exec_sql.ExecSQLJob] = Field(default=[], exclude=True)
    jobs_cache: dict[uuid.UUID, DB2FS | FS2DB | exec_sql.ExecSQLJob] = Field(
        default={}, exclude=True
    )

    @validator("jobs")
    def child_uniqueness_check(cls, value: list[DB2FS | FS2DB | exec_sql.ExecSQLJob]):
        validators.find_non_unique(value, "name")
        return value

    def get_job_by_id(self, jobs_id: uuid.UUID) -> DB2FS | FS2DB | exec_sql.ExecSQLJob:
        if len(self.jobs_cache) < 1:
            self.jobs_cache = {jobs.id: jobs for jobs in self.jobs}
        return self.jobs_cache[jobs_id]

    def get_jobs_of_type(
        self,
        job_type: Type[DB2FS] | Type[FS2DB] | Type[exec_sql.ExecSQLJob],
    ) -> list[DB2FS | FS2DB | exec_sql.ExecSQLJob]:
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
    ) -> list[exec_sql.ExecSQLJob]:
        """
        Filters the jobs list

        :return: List of jobs of the specified type
        """
        return [job for job in self.jobs if isinstance(job, exec_sql.ExecSQLJob)]
