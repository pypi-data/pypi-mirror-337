import logging
import uuid
from typing import Literal

from jinja2 import Environment, Template, TemplateSyntaxError
from pydantic import BaseModel, Field, validator

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
        alias_generator = writer.to_lower_camelcase

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
        alias_generator = writer.to_lower_camelcase

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
    """Base class for loading CLOE Schema model objects."""

    is_tsql: bool = Field(default=False, exclude=True)
    is_snowflake: bool = Field(default=False, exclude=True)
    name: str
    tables: list[DatabaseTable] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

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


class DatabaseDatabase(BaseModel):
    """Base class for loading CLOE Database model objects."""

    name: str
    schemas: list[DatabaseSchema] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

    @validator("name")
    def catalog_name_template(cls, value):
        try:
            Template(value)
            return value
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")

    @property
    def rendered_catalog_name(self) -> str:
        return Template(self.name).render()

    def get_ddl(self) -> str:
        return f"CREATE DATABASE {self.rendered_catalog_name};"


class Databases(BaseModel):
    model_id: str = "repository.db_full_catalog"
    model_content: list[DatabaseDatabase]
    tables_cache: dict[uuid.UUID, DatabaseTable] = Field({}, exclude=True)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {Template: lambda v: v.render()}
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

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
