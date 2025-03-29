import logging
import uuid

from jinja2 import Template, TemplateSyntaxError
from pydantic import validator

from cloecore.utils.model.jobs.base import BaseXToX
from cloecore.utils.model.repository.data_source_info import (
    DataSourceInfo,
    DataSourceInfos,
)
from cloecore.utils.model.repository.database import DatabaseTable
from cloecore.utils.model.repository.dataset import DatasetType, DatasetTypes

logger = logging.getLogger(__name__)


class DB2FS(BaseXToX):
    """Base class for loading CLOE DB2FS model objects."""

    container_name: str
    select_statement: Template
    dataset_types: DatasetTypes
    tables: dict[uuid.UUID, DatabaseTable]
    datasource_infos: DataSourceInfos
    dataset_type_id: uuid.UUID
    source_table_id: uuid.UUID
    datasource_info_id: uuid.UUID
    folder_path: Template | None = None
    sequence_column_name: str | None = None

    class Config:
        arbitrary_types_allowed = True

    @validator("select_statement", pre=True)
    def valid_jinja2_template(cls, value):
        try:
            template = Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return template

    @validator("folder_path", pre=True)
    def folder_path_valid_jinja2_template(cls, value):
        try:
            template = Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return template

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
        ].check_if_datasourceinfo_exists_by_id(value):
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
        return self.dataset_types.get_datasettype_by_id(self.dataset_type_id)

    @property
    def ds_info(self) -> DataSourceInfo:
        return self.datasource_infos.get_datasourceinfo_by_id(self.datasource_info_id)

    @property
    def rendered_folder_path(self) -> str:
        if self.folder_path is None:
            return self.ds_info.sourcesystem.name
        tenant_name = None
        if self.ds_info.tenant is not None:
            tenant_name = self.ds_info.tenant.name
        return self.folder_path.render(
            content=self.ds_info.content,
            sourcesystem_name=self.ds_info.sourcesystem.name,
            tenant=tenant_name,
            object_description=self.ds_info.object_description,
            ds_type_name=self.ds_type.name,
        )

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
        ds_info_name = self.datasource_infos.get_datasourceinfo_by_id(
            self.datasource_info_id
        ).sourcesystem.name
        ds_type_name = self.dataset_types.get_datasettype_by_id(
            self.dataset_type_id
        ).name
        ds_type_type = self.dataset_types.get_datasettype_by_id(
            self.dataset_type_id
        ).storage_format
        adf_delta_artifact = (
            f"{self.sequence_column_name} <= '$SEQUENCE_END' $SEQUENCE_START"
        )
        return self.select_statement.render(
            source_table_identifier=source_table_identifier,
            source_table=self.source_table,
            source_columns=self.source_table.columns,
            source_sourcesystem_name=ds_info_name,
            source_datasettype_name=ds_type_name,
            source_datasettype_type=ds_type_type,
            adf_delta_artifact=adf_delta_artifact,
        )
