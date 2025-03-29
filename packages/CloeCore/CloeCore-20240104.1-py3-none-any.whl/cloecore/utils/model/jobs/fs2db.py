from __future__ import annotations

import json
import logging
import pathlib
import uuid

from jinja2 import TemplateSyntaxError
from pydantic import Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils import templating_engine
from cloecore.utils.model.jobs.base import BaseXToX
from cloecore.utils.model.jobs.exec_sql import ExecSQL
from cloecore.utils.model.repository.database import DatabaseTable
from cloecore.utils.model.repository.dataset_type import DatasetType, DatasetTypes

logger = logging.getLogger(__name__)


class FS2DB(BaseXToX):
    """Base class for loading CLOE FS2DB model objects."""

    container_name: str
    filename_pattern: str
    folder_path_pattern: str
    dataset_types: DatasetTypes = Field(..., exclude=True)
    tables: dict[uuid.UUID, DatabaseTable] = Field(..., exclude=True)
    sink_table_id: uuid.UUID
    dataset_type_id: uuid.UUID
    get_from_filecatalog: bool = False
    exec_jobs: dict[uuid.UUID, ExecSQL] | dict = Field({}, exclude=True)
    post_load_exec_job_id: uuid.UUID | None = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("filename_pattern")
    def valid_jinja2_template(cls, value):
        try:
            templating_engine.get_jinja_env().from_string(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return value

    @validator("folder_path_pattern")
    def folder_path_valid_jinja2_template(cls, value):
        try:
            templating_engine.get_jinja_env().from_string(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return value

    @validator("dataset_type_id")
    def dataset_type_exists(cls, value, values, **kwargs):
        if "dataset_types" in values and not values[
            "dataset_types"
        ].check_if_dataset_type_exists_by_id(value):
            raise ValueError("dataset_type_id not in dataset_types")
        return value

    @validator("dataset_type_id")
    def dataset_type_implemented_for_sink(cls, value, values, **kwargs):
        if "dataset_types" in values and value in values["dataset_types"]:
            if values["dataset_types"][value].storage_format.lower() != "parquet":
                if not values["connections"][
                    values["sink_connection_id"]
                ].is_snowflake_nativ:
                    raise ValueError(
                        "dataset_type not implemented for sink connection."
                    )
        return value

    @validator("sink_table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @validator("post_load_exec_job_id")
    def exec_job_exists(cls, value, values, **kwargs):
        if "exec_jobs" in values and not values["exec_jobs"].check_if_job_exists_by_id(
            value
        ):
            raise ValueError("id not in exec_jobs")
        return value

    @property
    def sink_table(self) -> DatabaseTable:
        return self.tables[self.sink_table_id]

    @property
    def postload_execjob(self) -> ExecSQL | None:
        if self.post_load_exec_job_id is None:
            return None
        else:
            return self.exec_jobs[self.post_load_exec_job_id]

    @property
    def ds_type(self) -> DatasetType:
        return self.dataset_types.get_dataset_type_by_id(self.dataset_type_id)

    @property
    def filecatalog_wildcard(self) -> str:
        fc_wildcard = "%"
        for connection in self.connections.connections:
            if not connection.is_file_catalog_connection:
                continue
            if connection.is_snowflake_nativ:
                fc_wildcard = ".*"
        return fc_wildcard

    @property
    def rendered_filename_pattern(self) -> str:
        return (
            templating_engine.get_jinja_env()
            .from_string(self.filename_pattern)
            .render(
                ds_type_name=self.ds_type.name,
                ds_type_format=self.ds_type.storage_format,
                wildcard=self.filecatalog_wildcard,
            )
        )

    @property
    def rendered_folder_path_pattern(self) -> str:
        return (
            templating_engine.get_jinja_env()
            .from_string(self.folder_path_pattern)
            .render(
                ds_type_name=self.ds_type.name,
                ds_type_format=self.ds_type.storage_format,
                wildcard=self.filecatalog_wildcard,
            )
        )

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[FS2DB], list[ValidationError | json.JSONDecodeError]]:
        instances = []
        errors = []

        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        for file_path in input_path.iterdir():
            if file_path.is_file() and file_path.suffix == ".json":
                try:
                    with file_path.open("r") as file:
                        data = json.load(file)
                        instance = cls(**data)
                        instances.append(instance)
                except (ValidationError, json.JSONDecodeError) as e:
                    errors.append(e)

        return instances, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        content = self.json(indent=4, by_alias=True, exclude_none=True)
        writer.write_string_to_disk(content, output_path / f"{self.name}.json")
