import uuid
from typing import Literal

from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators


class DatasetType(BaseModel):
    """Base class for loading CLOE DatasetType model objects."""

    id: uuid.UUID
    name: str
    storage_format: Literal["CSV", "Parquet"]
    attributes: list | None

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)

    @property
    def is_parquet(self) -> bool:
        return self.storage_format.lower() == "parquet"

    @property
    def is_csv(self) -> bool:
        return self.storage_format.lower() == "csv"


class DatasetTypes(BaseModel):
    """Base class for loading CLOE DatasetType model objects."""

    datasettypes: list[DatasetType] = Field(default=[], exclude=True)

    datasettypes_cache: dict[uuid.UUID, DatasetType] = Field({}, exclude=True)

    @validator("datasettypes")
    def child_uniqueness_check(cls, value: list[DatasetType]):
        validators.find_non_unique(value, "name")
        return value

    def get_datasettype_by_id(self, datasettypes_id: uuid.UUID) -> DatasetType:
        if len(self.datasettypes_cache) < 1:
            self.datasettypes_cache = {
                datasettypes.id: datasettypes for datasettypes in self.datasettypes
            }
        return self.datasettypes_cache[datasettypes_id]

    def check_if_dataset_type_exists_by_id(self, dataset_types_id: uuid.UUID) -> bool:
        if len(self.datasettypes_cache) < 1:
            self.datasettypes_cache = {
                dataset_type.id: dataset_type for dataset_type in self.datasettypes
            }
        return dataset_types_id in self.datasettypes_cache
