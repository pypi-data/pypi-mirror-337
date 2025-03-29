from __future__ import annotations

import json
import logging
import pathlib
import uuid

from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators
from cloecore.utils.model.repository.database import DatabaseTable

logger = logging.getLogger(__name__)


class SPTableMapping(BaseModel):
    """SimplePipe TableMapping metadata model base class"""

    tables: dict[uuid.UUID, DatabaseTable] = Field(..., exclude=True)
    source_table_id: uuid.UUID
    sink_table_id: uuid.UUID
    order_by: int

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("source_table_id")
    def source_tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("source_table_id not in tables")
        return value

    @validator("sink_table_id")
    def sink_table_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("sink_table_id not in tables")
        return value

    @property
    def source_table(self) -> DatabaseTable:
        return self.tables[self.source_table_id]

    @property
    def sink_table(self) -> DatabaseTable:
        return self.tables[self.sink_table_id]


class SimplePipe(BaseModel):
    """SimplePipe metadata model base class"""

    name: str
    sql_pipe_template: str
    table_mappings: list[SPTableMapping]
    job_id: uuid.UUID | None = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("sql_pipe_template", pre=True)
    def valid_jinja2_template(cls, value):
        try:
            Template(value)
        except TemplateSyntaxError:
            raise ValueError("template is no valid jinja2 template")
        return value

    @validator("table_mappings")
    def min_number_table_mappings(cls, value):
        if len(value) < 1:
            raise ValueError("at least one table mapping needs to be set.")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[SimplePipe], list[ValidationError | json.JSONDecodeError]]:
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
