from __future__ import annotations

import json
import logging
import pathlib
import uuid

from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators
from cloecore.utils.model.modeler.powerpipe.ColumnMapping import PPColumnMapping
from cloecore.utils.model.modeler.powerpipe.Lookups import PPLookup
from cloecore.utils.model.modeler.powerpipe.SourceTable import PPSourceTable
from cloecore.utils.model.modeler.templates import SQLTemplate, SQLTemplates
from cloecore.utils.model.repository.database import DatabaseTable

logger = logging.getLogger(__name__)


class PowerPipe(BaseModel):
    """PowerPipe metadata model base class"""

    name: str
    tables: dict[uuid.UUID, DatabaseTable] = Field(..., exclude=True)
    sink_table_id: uuid.UUID
    templates: SQLTemplates = Field(..., exclude=True)
    sql_template_id: int
    job_id: uuid.UUID | None = None
    include_dq1: bool = True
    column_mappings: list[PPColumnMapping]
    include_dq2: bool = True
    include_dq3: bool = False
    log_dq1: bool = True
    log_dq2: bool = True
    log_dq3: bool = False
    source_tables: list[PPSourceTable]
    engine_templates: SQLTemplates = Field(..., exclude=True)
    lookups: list[PPLookup] | None = None
    post_processing_sql: str | None = None
    pre_processing_sql: str | None = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("sink_table_id")
    def tables_exists(cls, value, values, **kwargs):
        if "tables" in values and value not in values["tables"]:
            raise ValueError("id not in tables")
        return value

    @validator("sql_template_id")
    def template_exists(cls, value, values, **kwargs):
        if "templates" in values and not values[
            "templates"
        ].check_if_sql_template_exists_by_id(value):
            raise ValueError("id not in sql templates")
        return value

    @validator("column_mappings", each_item=True)
    def lookup_parameters_order_by_unique_check(
        cls, value: PPColumnMapping, values, **kwargs
    ):
        if (
            values.get("include_dq1", True)
            or values.get("include_dq2", True)
            or values.get("include_dq3", False)
        ):
            if value.calculation is not None and value.source_column_name is None:
                raise ValueError(
                    (
                        "source_column_name must be set if calculation is used and"
                        "dq is on"
                    )
                )
        return value

    @validator("column_mappings")
    def column_mapping_bk_check(cls, value: list[PPColumnMapping]):
        if any([column_mapping.bk_order is not None for column_mapping in value]):
            return value
        else:
            raise ValueError("no bk set.")

    @validator("include_dq2")
    def dq2_and_conversion_check(cls, value, values, **kwargs):
        if "column_mappings" in values and len(values["column_mappings"]) > 0:
            if any(
                [
                    column_mapping.convert_to_datatype is not None
                    for column_mapping in values["column_mappings"]
                ]
            ):
                return value
            else:
                logger.warning("DQ2 activated but no conversions. Deactivating DQ2.")
                return False
        return value

    @validator("log_dq2")
    def dq2_log_and_conversion_check(cls, value, values, **kwargs):
        if "column_mappings" in values and len(values["column_mappings"]) > 0:
            if any(
                [
                    column_mapping.is_logging_on_convert_error
                    for column_mapping in values["column_mappings"]
                ]
            ):
                return value
            else:
                logger.warning(
                    (
                        "DQ2 activated but no columns marked for logging."
                        " Deactivating DQ2 logging."
                    )
                )
                return False
        return value

    @validator("source_tables")
    def is_active_check(cls, value: list[PPSourceTable]):
        if all([not source_table.is_active for source_table in value]):
            raise ValueError("at least one source table must be active.")
        return value

    @property
    def sink_table(self) -> DatabaseTable:
        return self.tables[self.sink_table_id]

    @property
    def sqltemplate(self) -> SQLTemplate:
        return self.templates.get_template_by_id(self.sql_template_id)

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[PowerPipe], list[ValidationError | json.JSONDecodeError]]:
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
