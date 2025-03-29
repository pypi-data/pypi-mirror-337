import uuid

from pydantic import BaseModel, validator

from cloecore.utils.model import validators


class BatchstepDependency(BaseModel):
    """Base class for loading CLOE BatchstepDependency model objects."""

    dependent_on_batchstep_id: uuid.UUID
    ignore_dependency_failed_state: bool


class Batchstep(BaseModel):
    """Base class for loading Batchstep model objects."""

    id: uuid.UUID
    name: str
    job_id: uuid.UUID
    tags: str | None = None
    dependencies: list[BatchstepDependency] | None = None

    class Config:
        arbitrary_types_allowed = True

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("dependencies", each_item=True)
    def dependencies_self_dependency(cls, value: BatchstepDependency, values, **kwargs):
        if "id" in values and value.dependent_on_batchstep_id == values["id"]:
            raise ValueError("must not have a dependency on itself")
        return value

    def get_dependencies(self) -> list[uuid.UUID]:
        if self.dependencies is None:
            return []
        else:
            return [i.dependent_on_batchstep_id for i in self.dependencies]
