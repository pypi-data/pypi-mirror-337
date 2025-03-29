from __future__ import annotations

import json
import logging
import pathlib
import uuid
from typing import ClassVar

from jinja2 import TemplateSyntaxError
from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils import templating_engine
from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


class SQLTemplate(BaseModel):
    """SQLTemplate metadata model base class"""

    id: int
    name: str
    template: str
    description: str | None = None

    class Config:
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name = validator("name", allow_reuse=True)(validators.name_alphanumeric)

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[SQLTemplate], list[ValidationError | json.JSONDecodeError]]:
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

    @validator("template")
    def valid_jinja2_template(cls, value):
        try:
            templating_engine.get_jinja_env().from_string(value)
        except TemplateSyntaxError:
            raise ValueError("template is no valid jinja2 template")
        return value


class SQLTemplates(BaseModel):
    """Base class for loading CLOE SQLTemplate model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("sql_templates")

    sql_templates: list[SQLTemplate] = Field(default={}, exclude=True)
    sql_template_cache: dict[int, SQLTemplate] = Field({}, exclude=True)

    class Config:
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("sql_templates")
    def child_uniqueness_check(cls, value: list[SQLTemplate]):
        validators.find_non_unique(value, "name")
        return value

    def get_template_by_id(self, template_id: int) -> SQLTemplate:
        if len(self.sql_template_cache) < 1:
            self.sql_template_cache = {
                template.id: template for template in self.sql_templates
            }
        return self.sql_template_cache[template_id]

    def check_if_sql_template_exists_by_id(self, templates_id: uuid.UUID) -> bool:
        if len(self.sql_template_cache) < 1:
            self.sql_template_cache = {
                template.id: template for template in self.sql_templates
            }
        return templates_id in self.sql_template_cache

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[SQLTemplates, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = SQLTemplate.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(sql_templates=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.sql_templates:
            child.write_to_disk(output_path / self.subfolder_path)
