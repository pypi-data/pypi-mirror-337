import logging
import uuid

from pydantic import BaseModel, validator

from cloecore.utils.model import validators
from cloecore.utils.model.modeler.common import SQLTemplate
from cloecore.utils.model.repository.database import DatabaseTable

logger = logging.getLogger(__name__)


class PPLookupParameter(BaseModel):
    """PowerPipe LookupParameter metadata model base class"""

    source_column_name: str
    calculation: str | None
    order_by: int


class PPLookupReturnColumnMapping(BaseModel):
    """PowerPipe LookupReturnColumnMapping metadata model base class"""

    tables: dict[uuid.UUID, DatabaseTable]
    sink_table_id: uuid.UUID
    on_null_value: str
    return_column_name: str
    sink_column_name: str
    is_insert: bool = True
    is_update: bool = True
    is_logging_on_lookup_error: bool = False

    @validator("sink_table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @property
    def sink_table(self) -> DatabaseTable:
        return self.tables[self.sink_table_id]


class PPLookup(BaseModel):
    """PowerPipe Lookup metadata model base class"""

    name: str
    tables: dict[uuid.UUID, DatabaseTable]
    lookup_parameters: list[PPLookupParameter]
    lookup_table_id: uuid.UUID
    is_add_tenant_to_lookup_parameter: bool = False
    sink_lookup_bk_column_name: str | None = None
    lookup_column_name: str | None = None
    lookup_valid_parameter_column_name: str | None = None
    lookup_valid_from_column_name: str | None = None
    lookup_valid_to_column_name: str | None = None
    engine_templates: dict[int, SQLTemplate]
    return_column_mappings: list[PPLookupReturnColumnMapping]

    class Config:
        arbitrary_types_allowed = True

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("lookup_table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @validator("lookup_parameters")
    def lookup_parameters_order_by_unique_check(cls, value: list[PPLookupParameter]):
        order_number = []
        for lp in value:
            if lp.order_by not in order_number:
                order_number.append(lp.order_by)
            else:
                raise ValueError("order_by not unique")
        return value

    @validator("lookup_column_name")
    def lookup_parameters_if_column_name(cls, value, values, **kwargs):
        if "lookup_parameters" in values and len(values["lookup_parameters"]) > 0:
            return value
        else:
            raise ValueError("lookup column name set but no lookup parameters defined.")

    @property
    def lookup_source_table(self) -> DatabaseTable:
        return self.tables[self.lookup_table_id]

    @property
    def rendered_sink_bk_name(self) -> str:
        if self.sink_lookup_bk_column_name is None:
            return f"FK_{self.name}_BK"
        return self.sink_lookup_bk_column_name
