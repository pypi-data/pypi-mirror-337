import logging
import uuid

from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


class Tenant(BaseModel):
    """Base class for loading CLOE Tenant model objects."""

    id: uuid.UUID
    name: str

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)


class Tenants(BaseModel):
    """Base class for loading CLOE Tenant model objects."""

    tenants: list[Tenant] = Field(default=[], exclude=True)

    tenants_cache: dict[uuid.UUID, Tenant] = Field({}, exclude=True)

    @validator("tenants")
    def child_uniqueness_check(cls, value: list[Tenant]):
        validators.find_non_unique(value, "name")
        return value

    def get_tenant_by_id(self, tenants_id: uuid.UUID) -> Tenant:
        if len(self.tenants_cache) < 1:
            self.tenants_cache = {tenants.id: tenants for tenants in self.tenants}
        return self.tenants_cache[tenants_id]

    def check_if_tenant_exists_by_id(self, tenants_id: uuid.UUID) -> bool:
        if len(self.tenants_cache) < 1:
            self.tenants_cache = {tenant.id: tenant for tenant in self.tenants}
        return tenants_id in self.tenants_cache
