import logging
import uuid

from pydantic import BaseModel, root_validator, validator

from cloecore.utils.model.modeler.common import ConversionTemplate
from cloecore.utils.model.repository.database import DatabaseTable

logger = logging.getLogger(__name__)


class PPColumnMapping(BaseModel):
    """PowerPipe ColumnMapping metadata model base class"""

    source_column_name: str | None = None
    is_insert: bool = True
    is_update: bool = True
    is_load_on_convert_error: bool = True
    is_logging_on_convert_error: bool = True
    tables: dict[uuid.UUID, DatabaseTable]
    conversions: dict[str, ConversionTemplate]
    sink_table_id: uuid.UUID
    convert_to_datatype: str | None = None
    bk_order: int | None = None
    sink_column_name: str | None = None
    calculation: str | None = None
    on_convert_error_value: str | None = None
    on_null_value: str | None = None

    class Config:
        arbitrary_types_allowed = True

    @validator("sink_table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @validator("convert_to_datatype")
    def conversion_exists(cls, value, values, **kwargs):
        if "conversions" in values and value not in values["conversions"]:
            raise ValueError("type not in conversions")
        return value

    @root_validator
    def check_insert_correct(cls, values):
        bk, scn, calc = (
            values.get("bk_order"),
            values.get("source_column_name"),
            values.get("calculation"),
        )
        if bk is None and scn is None and calc is None:
            raise ValueError(
                (
                    "at least one of bk_order / source_column_name / calculation"
                    " need to be set."
                )
            )
        return values

    @root_validator
    def check_sink_correct(cls, values):
        bk, scn, insert, update = (
            values.get("bk_order"),
            values.get("sink_column_name"),
            values.get("is_insert"),
            values.get("is_update"),
        )
        if bk is None and scn is None and (insert is True or update is True):
            raise ValueError(
                (
                    "IsInsert or IsUpdate set to true but no bk_order and/or"
                    " SinkColumnName"
                )
            )
        return values

    @property
    def sink_table(self) -> DatabaseTable:
        return self.tables[self.sink_table_id]
