from __future__ import annotations

import json
import logging
import pathlib
import uuid
from typing import ClassVar

from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


class DatatypeTemplate(BaseModel):
    """DatatypeTemplate metadata model base class"""

    source_type: str
    parameter_template: str

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name = validator("source_type", allow_reuse=True)(
        validators.name_alphanumeric
    )

    @validator("parameter_template", pre=True)
    def valid_jinja2_template(cls, value):
        try:
            Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[DatatypeTemplate], list[ValidationError | json.JSONDecodeError]]:
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
        writer.write_string_to_disk(content, output_path / f"{self.source_type}.json")


class DatatypeTemplates(BaseModel):
    """Base class for loading CLOE DatatypeTemplate model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("datatype_templates")

    datatype_templates: list[DatatypeTemplate] = Field(default={}, exclude=True)
    datatype_template_cache: dict[str, DatatypeTemplate] = Field({}, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("datatype_templates")
    def child_uniqueness_check(cls, value: list[DatatypeTemplate]):
        validators.find_non_unique(value, "source_type")
        return value

    def get_template_by_id(self, template_id: str) -> DatatypeTemplate:
        if len(self.datatype_template_cache) < 1:
            self.datatype_template_cache = {
                template.source_type: template for template in self.datatype_templates
            }
        return self.datatype_template_cache[template_id]

    def check_if_datatype_template_exists_by_id(self, templates_id: uuid.UUID) -> bool:
        if len(self.datatype_template_cache) < 1:
            self.datatype_template_cache = {
                template.source_type: template for template in self.datatype_templates
            }
        return templates_id in self.datatype_template_cache

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[DatatypeTemplates, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = DatatypeTemplate.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(datatype_templates=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.datatype_templates:
            child.write_to_disk(output_path / self.subfolder_path)
