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


class ConversionTemplate(BaseModel):
    """ConversionTemplate metadata model base class"""

    output_type: str
    convert_template: str
    on_convert_error_default_value: str

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name = validator("output_name", allow_reuse=True)(
        validators.name_alphanumeric
    )

    @validator("convert_template", pre=True)
    def valid_jinja2_template(cls, value):
        try:
            Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[ConversionTemplate], list[ValidationError | json.JSONDecodeError]]:
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
        writer.write_string_to_disk(content, output_path / f"{self.output_type}.json")


class ConversionTemplates(BaseModel):
    """Base class for loading CLOE ConversionTemplate model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("conversion_templates")

    conversion_templates: list[ConversionTemplate] = Field(default={}, exclude=True)
    conversion_template_cache: dict[str, ConversionTemplate] = Field({}, exclude=True)

    @validator("conversion_templates")
    def child_uniqueness_check(cls, value: list[ConversionTemplate]):
        validators.find_non_unique(value, "output_type")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[ConversionTemplates, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = ConversionTemplate.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(conversion_templates=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.conversion_templates:
            child.write_to_disk(output_path / self.subfolder_path)

    def get_template_by_id(self, template_id: str) -> ConversionTemplate:
        if len(self.conversion_template_cache) < 1:
            self.conversion_template_cache = {
                template.output_type: template for template in self.conversion_templates
            }
        return self.conversion_template_cache[template_id]

    def check_if_conversion_template_exists_by_id(
        self, templates_id: uuid.UUID
    ) -> bool:
        if len(self.conversion_template_cache) < 1:
            self.conversion_template_cache = {
                template.output_type: template for template in self.conversion_templates
            }
        return templates_id in self.conversion_template_cache
