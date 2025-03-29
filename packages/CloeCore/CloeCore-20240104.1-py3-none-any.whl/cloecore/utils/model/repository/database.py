from __future__ import annotations

import json
import logging
import pathlib
import uuid
from typing import ClassVar, Literal

from jinja2 import Environment, Template, TemplateSyntaxError
from pydantic import BaseModel, Field, ValidationError, validator

from cloecore.utils import writer
from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


class TableColumn(BaseModel):
    """Base class for loading CLOE Column model objects."""

    comment: str | None = None
    constraints: str | None = None
    data_type: str
    data_type_length: int | None = None
    data_type_numeric_scale: int | None = None
    data_type_precision: int | None = None
    is_key: bool | None = None
    is_nullable: bool | None = None
    is_snowflake: bool = Field(default=False, exclude=True)
    is_tsql: bool = Field(default=False, exclude=True)
    table_level: str = Field(default="", exclude=True)
    labels: str | None = None
    name: str
    ordinal_position: int | None = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_table_columns
    )

    @property
    def rendered_name(self) -> str:
        name = self.name
        if self.is_tsql:
            name = f"[{name}]"
        if self.is_snowflake:
            name = f'"{name}"'
        return name


class DatabaseTable(BaseModel):
    """Base class for loading CLOE DatabaseTable model objects."""

    columns: list[TableColumn] = []
    id: uuid.UUID
    is_tsql: bool = Field(default=False, exclude=True)
    is_snowflake: bool = Field(default=False, exclude=True)
    level: Literal["src", "stg", "ver", "core", "derived", "lu"] | None = None
    name: str
    render_flag: bool = Field(default=False, exclude=True)
    schema_name: str = Field(..., exclude=True)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    _check_name = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_table_name
    )

    @validator("level", pre=True)
    def level_legacy(cls, value):
        if value is not None and value == "stage":
            return "stg"
        return value

    @property
    def is_version(self) -> bool:
        return self.level == "ver"

    @property
    def rendered_name(self) -> str:
        name = self.name
        if self.is_tsql:
            name = f"[{name}]"
        if self.is_snowflake:
            name = f'"{name}"'
        return name

    @property
    def rendered_schema_name(self) -> str:
        if self.is_tsql:
            return f"[{self.schema_name}]"
        if self.is_snowflake:
            return f'"{self.schema_name}"'
        return f"{self.schema_name}"

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path, schema_name: str
    ) -> tuple[list[DatabaseTable], list[ValidationError | json.JSONDecodeError]]:
        instances = []
        errors = []

        if not input_path.exists():
            logger.warning(
                f"Directory not found: {input_path}. Initialize without tables."
            )
            return [], []

        for file_path in input_path.iterdir():
            if file_path.is_file() and file_path.suffix == ".json":
                try:
                    with file_path.open("r") as file:
                        data = json.load(file)
                        instance = cls(**data, schema_name=schema_name)
                        instances.append(instance)
                except (ValidationError, json.JSONDecodeError) as e:
                    errors.append(e)

        return instances, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        content = self.json(indent=4, by_alias=True, exclude_none=True)
        writer.write_string_to_disk(content, output_path / f"{self.name}.json")

    def tsql(self) -> None:
        self.is_tsql = True
        for column in self.columns:
            column.is_tsql = True

    def snowflake(self) -> None:
        self.is_snowflake = True
        for column in self.columns:
            column.is_snowflake = True

    def get_table_identifier(
        self,
        name_prefix: str | None = None,
    ) -> str:
        """Gets the table sql identifier for sql queries. If set renders the jinja2 name
        template.

        Args:
            name_prefix (str | None, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        schema_name = self.rendered_schema_name
        table_name = self.rendered_name
        if name_prefix is not None:
            if self.is_tsql:
                table_name = f"[{name_prefix}{self.name}]"
            elif self.is_snowflake:
                table_name = f'"{name_prefix}{self.name}"'
            else:
                table_name = f"{name_prefix}{self.name}"
        name = f"{schema_name}.{table_name}"
        return name

    def get_ddl(self, template_env: Environment) -> str:
        ddl_template = template_env.get_template("create_table_ddl.sql.j2")
        if self.is_tsql:
            schema_name = f"[{self.schema_name}]"
        elif self.is_snowflake:
            schema_name = f'"{self.schema_name}"'
        else:
            schema_name = f"{self.schema_name}"
        return ddl_template.render(schema_name=schema_name, table=self)


class DatabaseSchema(BaseModel):
    """Base class for loading CLOE DatabaseSchema model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("tables")

    is_tsql: bool = Field(default=False, exclude=True)
    is_snowflake: bool = Field(default=False, exclude=True)
    name: str
    tables: list[DatabaseTable] = []

    @validator("tables")
    def child_uniqueness_check(cls, value: list[DatabaseTable]):
        validators.find_non_unique(value, "name")
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @property
    def rendered_name(self) -> str:
        name = self.name
        if self.is_tsql:
            name = f"[{name}]"
        if self.is_snowflake:
            name = f'"{name}"'
        return name

    def get_ddl(self) -> str:
        return f"CREATE SCHEMA {self.rendered_name};"

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[DatabaseSchema], list[ValidationError | json.JSONDecodeError]]:
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
                            (
                                tables,
                                sub_errors,
                            ) = DatabaseTable.read_instances_from_disk(
                                instance_folderpath, schema_name=data.get("name")
                            )
                            instance = cls(**data, tables=tables)
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
        for child in self.tables:
            child.write_to_disk(sub_output_path / self.subfolder_path)
        content = self.json(
            indent=4, by_alias=True, exclude_none=True, exclude={"tables"}
        )
        writer.write_string_to_disk(content, sub_output_path / f"{self.name}.json")


class DatabaseDatabase(BaseModel):
    """Base class for loading CLOE Database model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("schemas")

    name: str
    schemas: list[DatabaseSchema] = []
    is_tsql: bool = Field(default=False, exclude=True)
    is_snowflake: bool = Field(default=False, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("name")
    def catalog_name_template(cls, value):
        try:
            Template(value)
            return value
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")

    @validator("schemas")
    def child_uniqueness_check(cls, value: list[DatabaseSchema]):
        validators.find_non_unique(value, "name")
        return value

    @property
    def raw_rendered_name(self) -> str:
        return Template(self.name).render()

    @property
    def rendered_catalog_name(self) -> str:
        name = self.raw_rendered_name
        if self.is_tsql:
            name = f"[{name}]"
        if self.is_snowflake:
            name = f'"{name}"'
        return name

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[list[DatabaseDatabase], list[ValidationError | json.JSONDecodeError]]:
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
                            (
                                schemas,
                                sub_errors,
                            ) = DatabaseSchema.read_instances_from_disk(
                                instance_folderpath
                            )
                            instance = cls(**data, schemas=schemas)
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
        for child in self.schemas:
            child.write_to_disk(sub_output_path / self.subfolder_path)
        content = self.json(
            indent=4, by_alias=True, exclude_none=True, exclude={"schemas"}
        )
        writer.write_string_to_disk(content, sub_output_path / f"{self.name}.json")

    def tsql(self) -> None:
        self.is_tsql = True
        for schema in self.schemas:
            schema.is_tsql = True
            for table in schema.tables:
                table.tsql()

    def snowflake(self) -> None:
        self.is_snowflake = True
        for schema in self.schemas:
            schema.is_snowflake = True
            for table in schema.tables:
                table.snowflake()

    def get_ddl(self) -> str:
        return f"CREATE DATABASE {self.rendered_catalog_name};"


class Databases(BaseModel):
    """Base class for loading CLOE Databases model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("databases")

    model_id: str = "repository.db_full_catalog"
    model_content: list[DatabaseDatabase]
    tables_cache: dict[uuid.UUID, DatabaseTable] = Field({}, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("model_content")
    def child_uniqueness_check(cls, value: list[DatabaseDatabase]):
        validators.find_non_unique(value, "name")
        return value

    @property
    def tables(self) -> dict[uuid.UUID, DatabaseTable]:
        if len(self.tables_cache) < 1:
            self.tables_cache = {
                table.id: table
                for database in self.model_content
                for schema in database.schemas
                for table in schema.tables
            }
        return self.tables_cache

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[Databases, list[ValidationError | json.JSONDecodeError]]:
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances, errors = DatabaseDatabase.read_instances_from_disk(
            input_path / cls.subfolder_path
        )
        try:
            instance = cls(model_content=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.model_content:
            child.write_to_disk(output_path / self.subfolder_path)
