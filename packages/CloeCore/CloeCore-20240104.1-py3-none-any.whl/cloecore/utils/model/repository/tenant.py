from __future__ import annotations

import json
import logging
import pathlib
import uuid
from typing import ClassVar

from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


class Tenant(BaseModel):
    """Base class for loading CLOE Tenant model objects."""

    id: uuid.UUID
    name: str

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)

    class Config:
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[Tenant], list[ValidationError | json.JSONDecodeError]]:
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


class Tenants(BaseModel):
    """Base class for loading CLOE Tenant model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("tenants")

    tenants: list[Tenant] = Field(default=[], exclude=True)

    tenants_cache: dict[uuid.UUID, Tenant] = Field({}, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("tenants")
    def child_uniqueness_check(cls, value: list[Tenant]):
        validators.find_non_unique(value, "name")
        return value

    def get_tenant_by_id(self, tenants_id: uuid.UUID) -> Tenant:
        if len(self.tenants_cache) < 1:
            self.tenants_cache = {tenants.id: tenants for tenants in self.tenants}
        return self.tenants_cache[tenants_id]

    def check_if_tenant_exists_by_id(self, tenants_id: uuid.UUID) -> bool:
        if len(self.tenants_cache) < 1:
            self.tenants_cache = {tenant.id: tenant for tenant in self.tenants}
        return tenants_id in self.tenants_cache

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[Tenants, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = Tenant.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(tenants=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.tenants:
            child.write_to_disk(output_path / self.subfolder_path)
