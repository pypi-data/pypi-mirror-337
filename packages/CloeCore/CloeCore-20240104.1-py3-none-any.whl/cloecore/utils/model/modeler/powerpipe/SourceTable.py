import uuid

from pydantic import BaseModel, Field, validator

import cloecore.utils.writer as writer
from cloecore.utils.model.modeler.powerpipe.ColumnMapping import PPColumnMapping
from cloecore.utils.model.repository.database import DatabaseTable
from cloecore.utils.model.repository.tenant import Tenant, Tenants


class PPSourceTable(BaseModel):
    """PowerPipe SourceTable metadata model base class"""

    tables: dict[uuid.UUID, DatabaseTable] = Field(..., exclude=True)
    table_id: uuid.UUID
    order_by: int
    column_mappings: list[PPColumnMapping]
    is_active: bool = True
    tenants: Tenants | None = Field(default=None, exclude=True)
    tenant_id: uuid.UUID | None = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @validator("tenant_id")
    def tenants_exists(cls, value, values, **kwargs):
        if "tenants" in values and not values["tenants"].check_if_tenant_exists_by_id(
            value
        ):
            raise ValueError("tenant_id not in tenants")
        if "tenants" not in values:
            raise ValueError("tenant_id defined but no tenants defined")
        return value

    @property
    def source_table(self) -> DatabaseTable:
        return self.tables[self.table_id]

    @property
    def tenant(self) -> Tenant | None:
        if self.tenant_id is not None and self.tenants is not None:
            return self.tenants.get_tenant_by_id(self.tenant_id)
        return None
