import logging
import uuid

from pydantic import BaseModel, validator

from cloecore.utils.model import validators
from cloecore.utils.model.jobs.connections import Connection, Connections

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

    connections: Connections
    sink_connection_id: uuid.UUID
    source_connection_id: uuid.UUID

    class Config:
        arbitrary_types_allowed = True

    @validator("sink_connection_id")
    def sink_connection_exists(cls, value, values, **kwargs):
        if "connections" in values and not values[
            "connections"
        ].check_if_connection_exists_by_id(value):
            raise ValueError("sink_connection_id not in connections")
        return value

    @validator("source_connection_id")
    def source_connection_exists(cls, value, values, **kwargs):
        if "connections" in values and not values[
            "connections"
        ].check_if_connection_exists_by_id(value):
            raise ValueError("source_connection_id not in connections")
        return value

    @property
    def source_connection(self) -> Connection:
        return self.connections.get_connection_by_id(self.source_connection_id)

    @property
    def sink_connection(self) -> Connection:
        return self.connections.get_connection_by_id(self.sink_connection_id)
