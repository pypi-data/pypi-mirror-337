import logging
import uuid

from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, validator

from cloecore.utils.model import validators
from cloecore.utils.model.repository.database import DatabaseTable

logger = logging.getLogger(__name__)


class SPTableMapping(BaseModel):
    """SimplePipe TableMapping metadata model base class"""

    tables: dict[uuid.UUID, DatabaseTable]
    source_table_id: uuid.UUID
    sink_table_id: uuid.UUID
    order_by: int

    class Config:
        arbitrary_types_allowed = True

    @validator("source_table_id")
    def source_tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("source_table_id not in tables")
        return value

    @validator("sink_table_id")
    def sink_table_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("sink_table_id not in tables")
        return value

    @property
    def source_table(self) -> DatabaseTable:
        return self.tables[self.source_table_id]

    @property
    def sink_table(self) -> DatabaseTable:
        return self.tables[self.sink_table_id]


class SimplePipe(BaseModel):
    """SimplePipe metadata model base class"""

    name: str
    sql_pipe_template: Template
    table_mappings: list[SPTableMapping]
    job_id: uuid.UUID | None = None

    class Config:
        arbitrary_types_allowed = True

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("sql_pipe_template", pre=True)
    def valid_jinja2_template(cls, value):
        template = value
        try:
            template = Template(value)
        except TemplateSyntaxError:
            raise ValueError("template is no valid jinja2 template")
        return template

    @validator("table_mappings")
    def min_number_table_mappings(cls, value):
        if len(value) < 1:
            raise ValueError("at least one table mapping needs to be set.")
        return value
