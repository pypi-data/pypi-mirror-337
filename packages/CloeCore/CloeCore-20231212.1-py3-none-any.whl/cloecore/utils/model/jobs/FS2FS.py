"""Holds all methods and classes relevant to FS2FS jobs.
"""
import logging
import uuid

from pydantic import validator

from cloecore.utils.model.jobs.base import BaseXToX
from cloecore.utils.model.repository.dataset import DatasetType, DataSourceInfo

logger = logging.getLogger(__name__)


class FS2FS(BaseXToX):
    """Base class for loading CLOE FS2FS model objects."""

    source_container_name: str
    filename_pattern: str
    folder_path_pattern: str
    sink_container_name: str
    folder_path: str
    dataset_types: dict[uuid.UUID, DatasetType]
    datasource_infos: dict[uuid.UUID, DataSourceInfo]
    sink_dataset_type_id: uuid.UUID
    source_dataset_type_id: uuid.UUID
    datasource_info_id: uuid.UUID

    class Config:
        arbitrary_types_allowed = True

    @validator("sink_dataset_type_id")
    def sink_dataset_type_exists(cls, value, values, **kwargs):
        if "dataset_types" in values and value in values["dataset_types"]:
            raise ValueError("sink_dataset_type_id not in dataset_types")
        return value

    @validator("source_dataset_type_id")
    def source_dataset_type_exists(cls, value, values, **kwargs):
        if "dataset_types" in values and value in values["dataset_types"]:
            raise ValueError("source_dataset_type_id not in dataset_types")
        return value

    @validator("datasource_info_id")
    def data_source_infos_exists(cls, value, values, **kwargs):
        if "datasource_infos" in values and value in values["datasource_infos"]:
            raise ValueError("datasource_info_id not in datasource_infos")
        return value

    def get_sink_file_name(self) -> str:
        ds_info = self.datasource_infos[self.datasource_info_id]
        name = (
            f"{ds_info.sourcesystem.name}.{ds_info.object_description}"
            f".{ds_info.content}.{self.dataset_types[self.sink_dataset_type_id].name}"
        )
        return name

    @property
    def sink_ds_type(self) -> DatasetType:
        return self.dataset_types[self.source_dataset_type_id]
