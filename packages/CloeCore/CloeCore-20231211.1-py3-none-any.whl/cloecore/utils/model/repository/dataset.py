import uuid
from typing import Literal

from pydantic import BaseModel, validator

from cloecore.utils.model import validators
from cloecore.utils.model.repository.tenant import Tenant


class Sourcesystem(BaseModel):
    """Base class for loading CLOE Sourcesystem model objects."""

    id: uuid.UUID
    name: str

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)


class DataSourceInfo(BaseModel):
    """Base class for loading CLOE DataSourceInfo model objects."""

    id: uuid.UUID
    content: Literal["full", "delta"]
    sourcesystems: dict[uuid.UUID, Sourcesystem]
    sourcesystem_id: uuid.UUID
    tenants: dict[uuid.UUID, Tenant]
    tenant_id: uuid.UUID | None = None
    object_description: str | None = None

    @validator("tenant_id")
    def tenants_exists(cls, value, values, **kwargs):
        if "tenants" in values and value not in values["tenants"]:
            raise ValueError("tenant_id not in tenants")
        return value

    @validator("sourcesystem_id")
    def sourcesystem_exists(cls, value, values, **kwargs):
        if "sourcesystems" in values and value not in values["sourcesystems"]:
            raise ValueError("sourcesystem_id not in sourcesystems")
        return value

    class Config:
        arbitrary_types_allowed = True

    @property
    def sourcesystem(self) -> Sourcesystem:
        return self.sourcesystems[self.sourcesystem_id]

    @property
    def tenant(self) -> Tenant | None:
        if self.tenant_id is not None:
            return self.tenants[self.tenant_id]
        return None


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
