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
from cloecore.utils.model.repository.data_source_info import (
    DataSourceInfo,
    DataSourceInfos,
)
from cloecore.utils.model.repository.database import DatabaseTable
from cloecore.utils.model.repository.dataset_type import DatasetType, DatasetTypes

logger = logging.getLogger(__name__)


class DB2FS(BaseXToX):
    """Base class for loading CLOE DB2FS model objects."""

    container_name: str
    select_statement: str
    dataset_types: DatasetTypes = Field(..., exclude=True)
    tables: dict[uuid.UUID, DatabaseTable] = Field(..., exclude=True)
    datasource_infos: DataSourceInfos = Field(..., exclude=True)
    dataset_type_id: uuid.UUID
    source_table_id: uuid.UUID
    datasource_info_id: uuid.UUID
    folder_path: str | None = None
    sequence_column_name: str | None = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("select_statement")
    def valid_jinja2_template(cls, value):
        try:
            templating_engine.get_jinja_env().from_string(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return value

    @validator("folder_path")
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

    @validator("datasource_infos")
    def data_source_infos_exists(cls, value, values, **kwargs):
        if "datasource_infos" in values and not values[
            "datasource_infos"
        ].check_if_data_source_info_exists_by_id(value):
            raise ValueError("datasource_info_id not in datasource_infos")
        return value

    @validator("source_table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @property
    def source_table(self) -> DatabaseTable:
        return self.tables[self.source_table_id]

    @property
    def ds_type(self) -> DatasetType:
        return self.dataset_types.get_dataset_type_by_id(self.dataset_type_id)

    @property
    def ds_info(self) -> DataSourceInfo:
        return self.datasource_infos.get_data_source_info_by_id(self.datasource_info_id)

    @property
    def rendered_folder_path(self) -> str:
        if self.folder_path is None:
            return self.ds_info.sourcesystem.name
        tenant_name = None
        if self.ds_info.tenant is not None:
            tenant_name = self.ds_info.tenant.name
        return (
            templating_engine.get_jinja_env()
            .from_string(self.folder_path)
            .render(
                content=self.ds_info.content,
                sourcesystem_name=self.ds_info.sourcesystem.name,
                tenant=tenant_name,
                object_description=self.ds_info.object_description,
                ds_type_name=self.ds_type.name,
            )
        )

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[DB2FS], list[ValidationError | json.JSONDecodeError]]:
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

    def get_sink_file_name(self) -> str:
        ds_info = self.ds_info
        name = f"{ds_info.sourcesystem.name}."
        if ds_info.tenant is not None:
            name += f"{ds_info.tenant.name}."
        name += f"{ds_info.object_description}.{ds_info.content}.{self.ds_type.name}"
        return name

    def render_select_statement(self) -> str:
        source_table_identifier = self.source_connection.get_object_identifier(
            schema_name=self.source_table.schema_name,
            object_name=self.source_table.name,
        )
        ds_info_name = self.datasource_infos.get_data_source_info_by_id(
            self.datasource_info_id
        ).sourcesystem.name
        ds_type_name = self.dataset_types.get_dataset_type_by_id(
            self.dataset_type_id
        ).name
        ds_type_type = self.dataset_types.get_dataset_type_by_id(
            self.dataset_type_id
        ).storage_format
        adf_delta_artifact = (
            f"{self.sequence_column_name} <= '$SEQUENCE_END' $SEQUENCE_START"
        )
        return (
            templating_engine.get_jinja_env()
            .from_string(self.select_statement)
            .render(
                source_table_identifier=source_table_identifier,
                source_table=self.source_table,
                source_columns=self.source_table.columns,
                source_sourcesystem_name=ds_info_name,
                source_datasettype_name=ds_type_name,
                source_datasettype_type=ds_type_type,
                adf_delta_artifact=adf_delta_artifact,
            )
        )
