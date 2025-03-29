from __future__ import annotations

import json
import pathlib
import uuid
from typing import ClassVar

from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators


class Sourcesystem(BaseModel):
    """Base class for loading CLOE Sourcesystem model objects."""

    id: uuid.UUID
    name: str

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)

    class Config:
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[Sourcesystem], list[ValidationError | json.JSONDecodeError]]:
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


class Sourcesystems(BaseModel):
    """Base class for loading CLOE Sourcesystem model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("sourcesystems")

    sourcesystems: list[Sourcesystem] = Field(default=[], exclude=True)

    sourcesystems_cache: dict[uuid.UUID, Sourcesystem] = Field({}, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

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

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[Sourcesystems, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = Sourcesystem.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(sourcesystems=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.sourcesystems:
            child.write_to_disk(output_path / self.subfolder_path)
