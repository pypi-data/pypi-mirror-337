import uuid

from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators


class Sourcesystem(BaseModel):
    """Base class for loading CLOE Sourcesystem model objects."""

    id: uuid.UUID
    name: str

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)


class Sourcesystems(BaseModel):
    """Base class for loading CLOE Sourcesystem model objects."""

    sourcesystems: list[Sourcesystem] = Field(default=[], exclude=True)

    sourcesystems_cache: dict[uuid.UUID, Sourcesystem] = Field({}, exclude=True)

    @validator("sourcesystems")
    def child_uniqueness_check(cls, value: list[Sourcesystem]):
        validators.find_non_unique(value, "name")
        return value

    def get_sourcesystem_by_id(self, sourcesystems_id: uuid.UUID) -> Sourcesystem:
        if len(self.sourcesystems_cache) < 1:
            self.sourcesystems_cache = {
                sourcesystems.id: sourcesystems for sourcesystems in self.sourcesystems
            }
        return self.sourcesystems_cache[sourcesystems_id]

    def check_if_sourcesystem_exists_by_id(self, sourcesystems_id: uuid.UUID) -> bool:
        if len(self.sourcesystems_cache) < 1:
            self.sourcesystems_cache = {
                sourcesystem.id: sourcesystem for sourcesystem in self.sourcesystems
            }
        return sourcesystems_id in self.sourcesystems_cache
