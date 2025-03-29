import uuid
from typing import Literal

from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators
from cloecore.utils.model.repository import sourcesystem, tenant


class DataSourceInfo(BaseModel):
    """Base class for loading CLOE DataSourceInfo model objects."""

    id: uuid.UUID
    content: Literal["full", "delta"]
    sourcesystems: sourcesystem.Sourcesystems
    sourcesystem_id: uuid.UUID
    tenants: tenant.Tenants
    tenant_id: uuid.UUID | None = None
    object_description: str | None = None

    @validator("tenant_id")
    def tenants_exists(cls, value, values, **kwargs):
        if "tenants" in values and not values["tenants"].check_if_tenant_exists_by_id(
            value
        ):
            raise ValueError("tenant_id not in tenants")
        return value

    @validator("sourcesystem_id")
    def sourcesystem_exists(cls, value, values, **kwargs):
        if "sourcesystems" in values and not values[
            "sourcesystems"
        ].check_if_sourcesystem_exists_by_id(value):
            raise ValueError("sourcesystem_id not in sourcesystems")
        return value

    class Config:
        arbitrary_types_allowed = True

    @property
    def sourcesystem(self) -> sourcesystem.Sourcesystem:
        return self.sourcesystems.get_sourcesystem_by_id(self.sourcesystem_id)

    @property
    def tenant(self) -> tenant.Tenant | None:
        if self.tenant_id is not None:
            return self.tenants.get_tenant_by_id(self.tenant_id)
        return None


class DataSourceInfos(BaseModel):
    """Base class for loading CLOE Datasourceinfo model objects."""

    datasourceinfos: list[DataSourceInfo] = Field(default=[], exclude=True)

    datasourceinfos_cache: dict[uuid.UUID, DataSourceInfo] = Field({}, exclude=True)

    @validator("datasourceinfos")
    def child_uniqueness_check(cls, value: list[DataSourceInfo]):
        validators.find_non_unique(value, "object_description")
        return value

    def get_datasourceinfo_by_id(self, datasourceinfos_id: uuid.UUID) -> DataSourceInfo:
        if len(self.datasourceinfos_cache) < 1:
            self.datasourceinfos_cache = {
                datasourceinfos.id: datasourceinfos
                for datasourceinfos in self.datasourceinfos
            }
        return self.datasourceinfos_cache[datasourceinfos_id]

    def check_if_datasourceinfo_exists_by_id(
        self, datasourceinfos_id: uuid.UUID
    ) -> bool:
        if len(self.datasourceinfos_cache) < 1:
            self.datasourceinfos_cache = {
                datasourceinfo.id: datasourceinfo
                for datasourceinfo in self.datasourceinfos
            }
        return datasourceinfos_id in self.datasourceinfos_cache
