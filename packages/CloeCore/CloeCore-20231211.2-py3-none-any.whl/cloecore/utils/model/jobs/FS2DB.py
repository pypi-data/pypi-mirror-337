import logging
import uuid

from jinja2 import Template, TemplateSyntaxError
from pydantic import validator

from cloecore.utils.model.jobs.base import BaseXToX
from cloecore.utils.model.jobs.Exec_SQL import ExecSQLJob
from cloecore.utils.model.repository.database import DatabaseTable
from cloecore.utils.model.repository.dataset import DatasetType

logger = logging.getLogger(__name__)


class FS2DB(BaseXToX):
    """Base class for loading CLOE FS2DB model objects."""

    container_name: str
    filename_pattern: Template
    folder_path_pattern: Template
    dataset_types: dict[uuid.UUID, DatasetType]
    tables: dict[uuid.UUID, DatabaseTable]
    sink_table_id: uuid.UUID
    dataset_type_id: uuid.UUID
    get_from_filecatalog: bool = False
    exec_jobs: dict[uuid.UUID, ExecSQLJob] | dict = {}
    post_load_exec_job_id: uuid.UUID | None = None

    class Config:
        arbitrary_types_allowed = True

    @validator("filename_pattern", pre=True)
    def valid_jinja2_template(cls, value):
        try:
            template = Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return template

    @validator("folder_path_pattern", pre=True)
    def folder_path_valid_jinja2_template(cls, value):
        try:
            template = Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return template

    @validator("dataset_type_id")
    def dataset_type_exists(cls, value, values, **kwargs):
        if "dataset_types" in values and value not in values["dataset_types"]:
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
        if "exec_jobs" in values and value not in values["exec_jobs"]:
            raise ValueError("id not in exec_jobs")
        return value

    @property
    def sink_table(self) -> DatabaseTable:
        return self.tables[self.sink_table_id]

    @property
    def postload_execjob(self) -> ExecSQLJob | None:
        if self.post_load_exec_job_id is None:
            return None
        else:
            return self.exec_jobs[self.post_load_exec_job_id]

    @property
    def ds_type(self) -> DatasetType:
        return self.dataset_types[self.dataset_type_id]

    @property
    def filecatalog_wildcard(self) -> str:
        fc_wildcard = "%"
        for connection in self.connections.values():
            if not connection.is_file_catalog_connection:
                continue
            if connection.is_snowflake_nativ:
                fc_wildcard = ".*"
        return fc_wildcard

    @property
    def rendered_filename_pattern(self) -> str:
        return self.filename_pattern.render(
            ds_type_name=self.ds_type.name,
            ds_type_format=self.ds_type.storage_format,
            wildcard=self.filecatalog_wildcard,
        )

    @property
    def rendered_folder_path_pattern(self) -> str:
        return self.folder_path_pattern.render(
            ds_type_name=self.ds_type.name,
            ds_type_format=self.ds_type.storage_format,
            wildcard=self.filecatalog_wildcard,
        )
