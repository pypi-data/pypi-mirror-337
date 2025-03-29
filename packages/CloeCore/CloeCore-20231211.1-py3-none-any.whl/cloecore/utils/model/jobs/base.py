import logging
import uuid

from pydantic import BaseModel, validator

from cloecore.utils.model import validators
from cloecore.utils.model.jobs.connections import Connection

logger = logging.getLogger(__name__)


class BaseJob(BaseModel):
    """Base class for loading CLOE Job model objects."""

    description: str | None = None
    id: uuid.UUID
    name: str

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    def get_short_id(self) -> str:
        return str(self.id).split("-")[0][:6]


class BaseXToX(BaseJob):
    """Base class for loading CLOE XToX Job model objects."""

    connections: dict[uuid.UUID, Connection]
    sink_connection_id: uuid.UUID
    source_connection_id: uuid.UUID

    class Config:
        arbitrary_types_allowed = True

    @validator("connections")
    def file_catalog_connection_exists(cls, value, values, **kwargs):
        if "connections" in values and any(
            connection.is_file_catalog_connection
            for connection in values["connections"]
        ):
            raise ValueError("at least one filecatalog connection must be defined.")
        return value

    @validator("connections", each_item=True)
    def file_catalog_connection_allowed(cls, value, values, **kwargs):
        if value.is_file_catalog_connection:
            if not (value.is_snowflake_nativ or value.is_tsql):
                raise ValueError(
                    "'%s' system type not allowed as filecatalog location.",
                    values.system_type,
                )
        return value

    @validator("sink_connection_id")
    def sink_connection_exists(cls, value, values, **kwargs):
        if "connections" in values and value not in values["connections"]:
            raise ValueError("sink_connection_id not in connections")
        return value

    @validator("source_connection_id")
    def source_connection_exists(cls, value, values, **kwargs):
        if "connections" in values and value not in values["connections"]:
            raise ValueError("source_connection_id not in connections")
        return value

    @property
    def source_connection(self) -> Connection:
        return self.connections[self.source_connection_id]

    @property
    def sink_connection(self) -> Connection:
        return self.connections[self.sink_connection_id]
