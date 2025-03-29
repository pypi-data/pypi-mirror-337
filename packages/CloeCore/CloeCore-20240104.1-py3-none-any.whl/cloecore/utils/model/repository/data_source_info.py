from __future__ import annotations

import json
import pathlib
import uuid
from typing import ClassVar, Literal

from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators
from cloecore.utils.model.repository import sourcesystem, tenant


class DataSourceInfo(BaseModel):
    """Base class for loading CLOE DataSourceInfo model objects."""

    id: uuid.UUID
    content: Literal["full", "delta"]
    sourcesystems: sourcesystem.Sourcesystems = Field(..., exclude=True)
    sourcesystem_id: uuid.UUID
    tenants: tenant.Tenants = Field(..., exclude=True)
    tenant_id: uuid.UUID | None = None
    object_description: str | None = None

    _check_name = validator("object_description", allow_reuse=True)(
        validators.name_alphanumeric
    )

    @validator("tenant_id")
    def tenants_exists(cls, value, values, **kwargs):
        if "tenants" in values and not values["tenants"].check_if_tenant_exists_by_id(
            value
        ):
            raise ValueError("tenant_id not in tenants")
        return value

    @validator("sourcesystem_id")
    def sourcesystem_exists(cls, value, values, **kwargs):
        if "sourcesystems" in values and not values[
            "sourcesystems"
        ].check_if_sourcesystem_exists_by_id(value):
            raise ValueError("sourcesystem_id not in sourcesystems")
        return value

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @property
    def sourcesystem(self) -> sourcesystem.Sourcesystem:
        return self.sourcesystems.get_sourcesystem_by_id(self.sourcesystem_id)

    @property
    def tenant(self) -> tenant.Tenant | None:
        if self.tenant_id is not None:
            return self.tenants.get_tenant_by_id(self.tenant_id)
        return None

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[DataSourceInfo], list[ValidationError | json.JSONDecodeError]]:
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
        writer.write_string_to_disk(
            content, output_path / f"{self.object_description}.json"
        )


class DataSourceInfos(BaseModel):
    """Base class for loading CLOE DataSourceInfos model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("data_source_infos")

    data_source_infos: list[DataSourceInfo] = Field(default=[], exclude=True)

    data_source_infos_cache: dict[uuid.UUID, DataSourceInfo] = Field({}, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("data_source_infos")
    def child_uniqueness_check(cls, value: list[DataSourceInfo]):
        validators.find_non_unique(value, "object_description")
        return value

    def get_data_source_info_by_id(
        self, data_source_info_id: uuid.UUID
    ) -> DataSourceInfo:
        if len(self.data_source_infos_cache) < 1:
            self.data_source_infos_cache = {
                data_source_info.id: data_source_info
                for data_source_info in self.data_source_infos
            }
        return self.data_source_infos_cache[data_source_info_id]

    def check_if_data_source_info_exists_by_id(
        self, data_source_info_id: uuid.UUID
    ) -> bool:
        if len(self.data_source_infos_cache) < 1:
            self.data_source_infos_cache = {
                data_source_info.id: data_source_info
                for data_source_info in self.data_source_infos
            }
        return data_source_info_id in self.data_source_infos_cache

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[DataSourceInfos, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = DataSourceInfo.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(data_source_infos=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.data_source_infos:
            child.write_to_disk(output_path / self.subfolder_path)
