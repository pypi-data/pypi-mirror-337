from __future__ import annotations

import json
import pathlib
import uuid
from typing import ClassVar

from croniter import croniter
from pydantic import BaseModel, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators
from cloecore.utils.model.batch.batchstep import Batchstep


class Batch(BaseModel):
    """Base class for loading CLOE Batch model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("batchsteps")

    name: str
    cron: str
    batchsteps: list[Batchstep]
    timezone: str = "W. Europe Standard Time"
    tags: str | None = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

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

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[Batch], list[ValidationError | json.JSONDecodeError]]:
        instances = []
        errors = []

        if not input_path.exists() or not input_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        for instance_dir in input_path.iterdir():
            if instance_dir.is_dir():
                json_files = list(instance_dir.glob("*.json"))
                if json_files:
                    json_file = json_files[0]
                    try:
                        with json_file.open("r") as file:
                            data = json.load(file)
                            instance_folderpath = instance_dir / cls.subfolder_path
                            batchsteps, sub_errors = Batchstep.read_instances_from_disk(
                                instance_folderpath
                            )
                            instance = cls(**data, batchsteps=batchsteps)
                            instances.append(instance)
                            errors += sub_errors

                    except (ValidationError, json.JSONDecodeError) as e:
                        errors.append(e)
                        errors += sub_errors
                else:
                    raise FileNotFoundError(
                        f"No JSON file found in directory: {instance_dir}"
                    )

        return instances, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        sub_output_path = output_path / f"{self.name}"
        for child in self.batchsteps:
            child.write_to_disk(sub_output_path / self.subfolder_path)
        content = self.json(
            indent=4, by_alias=True, exclude_none=True, exclude={"batchsteps"}
        )
        writer.write_string_to_disk(content, sub_output_path / f"{self.name}.json")

    def get_batchstep_by_id(self, id: uuid.UUID):
        for batchstep in self.batchsteps:
            if batchstep.id == id:
                return batchstep


class Batches(BaseModel):
    """Base class for loading CLOE Batch model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("batches")

    batches: list[Batch] = []

    @validator("batches")
    def child_uniqueness_check(cls, value: list[Batch]):
        validators.find_non_unique(value, "name")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[Batches, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = Batch.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(batches=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.batches:
            child.write_to_disk(output_path / self.subfolder_path)
