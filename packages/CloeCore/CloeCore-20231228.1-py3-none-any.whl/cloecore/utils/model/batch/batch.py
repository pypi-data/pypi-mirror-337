import uuid

from croniter import croniter
from pydantic import BaseModel, validator

from cloecore.utils.model import validators
from cloecore.utils.model.batch.batchstep import Batchstep


class Batch(BaseModel):
    """Base class for loading CLOE Batch model objects."""

    name: str
    cron: str
    batchsteps: list[Batchstep]
    timezone: str = "W. Europe Standard Time"
    tags: str | None = None

    class Config:
        arbitrary_types_allowed = True

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("cron")
    def cron_valid_check(cls, value):
        if not croniter.is_valid(value):
            raise ValueError("is not a valid cron")
        return value

    @validator("batchsteps")
    def child_uniqueness_check(cls, value):
        validators.find_non_unique(value, "name")
        return value

    def get_batchstep_by_id(self, id: uuid.UUID):
        for batchstep in self.batchsteps:
            if batchstep.id == id:
                return batchstep


class Batches(BaseModel):
    """Base class for loading CLOE Batch model objects."""

    batches: dict[uuid.UUID, Batch]

    @validator("batches")
    def child_uniqueness_check(cls, value: dict[uuid.UUID, Batch]):
        validators.find_non_unique(list(value.values()), "name")
        return value
