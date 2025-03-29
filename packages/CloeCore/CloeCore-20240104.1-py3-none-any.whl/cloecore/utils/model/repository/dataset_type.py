from __future__ import annotations

import json
import pathlib
import uuid
from typing import ClassVar, Literal

from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators


class DatasetType(BaseModel):
    """Base class for loading CLOE DatasetType model objects."""

    id: uuid.UUID
    name: str
    storage_format: Literal["CSV", "Parquet"]
    attributes: list | None

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)

    class Config:
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @property
    def is_parquet(self) -> bool:
        return self.storage_format.lower() == "parquet"

    @property
    def is_csv(self) -> bool:
        return self.storage_format.lower() == "csv"

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[DatasetType], list[ValidationError | json.JSONDecodeError]]:
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


class DatasetTypes(BaseModel):
    """Base class for loading CLOE DatasetType model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("dataset_types")

    dataset_types: list[DatasetType] = Field(default=[], exclude=True)

    dataset_types_cache: dict[uuid.UUID, DatasetType] = Field({}, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("dataset_types")
    def child_uniqueness_check(cls, value: list[DatasetType]):
        validators.find_non_unique(value, "name")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[DatasetTypes, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = DatasetType.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(dataset_types=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.dataset_types:
            child.write_to_disk(output_path / self.subfolder_path)

    def get_dataset_type_by_id(self, dataset_types_id: uuid.UUID) -> DatasetType:
        if len(self.dataset_types_cache) < 1:
            self.dataset_types_cache = {
                dataset_types.id: dataset_types for dataset_types in self.dataset_types
            }
        return self.dataset_types_cache[dataset_types_id]

    def check_if_dataset_type_exists_by_id(self, dataset_types_id: uuid.UUID) -> bool:
        if len(self.dataset_types_cache) < 1:
            self.dataset_types_cache = {
                dataset_type.id: dataset_type for dataset_type in self.dataset_types
            }
        return dataset_types_id in self.dataset_types_cache
