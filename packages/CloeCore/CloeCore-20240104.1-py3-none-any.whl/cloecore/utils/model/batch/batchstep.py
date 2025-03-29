from __future__ import annotations

import json
import pathlib
import uuid

from pydantic import BaseModel, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators


class BatchstepDependency(BaseModel):
    """Base class for loading CLOE BatchstepDependency model objects."""

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

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
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("dependencies", each_item=True)
    def dependencies_self_dependency(cls, value: BatchstepDependency, values, **kwargs):
        if "id" in values and value.dependent_on_batchstep_id == values["id"]:
            raise ValueError("must not have a dependency on itself")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[Batchstep], list[ValidationError | json.JSONDecodeError]]:
        instances = []
        errors = []

        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        for file_path in input_path.iterdir():
            if file_path.is_file() and file_path.suffix == ".json":
                try:
                    with file_path.open("r") as file:
                        data = json.load(file)
                        instance = cls(**data)
                        instances.append(instance)
                except (ValidationError, json.JSONDecodeError) as e:
                    errors.append(e)

        return instances, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        content = self.json(indent=4, by_alias=True, exclude_none=True)
        writer.write_string_to_disk(content, output_path / f"{self.name}.json")

    def get_dependencies(self) -> list[uuid.UUID]:
        if self.dependencies is None:
            return []
        else:
            return [i.dependent_on_batchstep_id for i in self.dependencies]
