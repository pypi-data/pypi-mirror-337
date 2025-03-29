import logging
import uuid

from pydantic import BaseModel, validator

from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


class Tenant(BaseModel):
    """Base class for loading CLOE Tenant model objects."""

    id: uuid.UUID
    name: str

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)
