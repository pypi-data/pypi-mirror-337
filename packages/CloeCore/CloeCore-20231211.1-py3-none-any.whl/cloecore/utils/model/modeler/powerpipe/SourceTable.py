import uuid

from pydantic import BaseModel, validator

from cloecore.utils.model.modeler.powerpipe.ColumnMapping import PPColumnMapping
from cloecore.utils.model.repository.database import DatabaseTable
from cloecore.utils.model.repository.tenant import Tenant


class PPSourceTable(BaseModel):
    """PowerPipe SourceTable metadata model base class"""

    tables: dict[uuid.UUID, DatabaseTable]
    table_id: uuid.UUID
    order_by: int
    column_mappings: list[PPColumnMapping]
    is_active: bool = True
    tenants: dict[uuid.UUID, Tenant] | None = None
    tenant_id: uuid.UUID | None = None

    class Config:
        arbitrary_types_allowed = True

    @validator("table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @validator("tenant_id")
    def tenants_exists(cls, value, values, **kwargs):
        if "tenants" in values and value not in values["tenants"]:
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
            return self.tenants[self.tenant_id]
        return None
