import logging
import uuid
from typing import ClassVar

from pydantic import BaseModel, validator

from cloecore.utils.model import validators
from cloecore.utils.templating_engine.general_templates import env

logger = logging.getLogger(__name__)


class Connection(BaseModel):
    """Base class for loading CLOE Connection model objects."""

    azure_synapse_key: ClassVar[str] = "Azure Synapse Analytics"
    sql_server_nativ_key: ClassVar[str] = "SQL Server >=2016"
    azure_server_nativ_key: ClassVar[str] = "Azure SQL Server"
    snowflake_nativ_key: ClassVar[str] = "Snowflake"
    azure_blob_key: ClassVar[str] = "AzureBlob"
    oracle_key: ClassVar[str] = "Oracle"
    db2_key: ClassVar[str] = "DB2"
    postgresql_key: ClassVar[str] = "PostgreSQL"
    azurepostgresql_key: ClassVar[str] = "AzurePostgreSQL"
    connection_string_secret_name: str
    id: uuid.UUID
    name: str
    system_type: str
    service_level: str | None = None
    is_file_catalog_connection: bool = False

    _check_name_w_replace = validator("name", allow_reuse=True)(
        validators.name_alphanumeric_w_replace
    )

    @validator("system_type")
    def available_system_type(cls, value):
        available_systems = [
            cls.azure_synapse_key,
            cls.sql_server_nativ_key,
            cls.azure_server_nativ_key,
            cls.snowflake_nativ_key,
            cls.azure_blob_key,
            cls.oracle_key,
            cls.db2_key,
            cls.postgresql_key,
            cls.azurepostgresql_key,
        ]
        if value not in available_systems:
            raise ValueError("unknown system type")
        return value

    @validator("is_file_catalog_connection")
    def file_catalog_available(cls, value, values, **kwargs):
        if value:
            available_systems = [
                cls.azure_synapse_key,
                cls.azure_server_nativ_key,
                cls.snowflake_nativ_key,
            ]
            if (
                "system_type" in values
                and values["system_type"] not in available_systems
            ):
                raise ValueError("not allowed as filecatalog database.")
        return value

    @property
    def is_snowflake_nativ(self) -> bool:
        return self.system_type == self.snowflake_nativ_key

    @property
    def is_azure_sql_nativ(self) -> bool:
        return self.system_type == self.azure_server_nativ_key

    @property
    def is_sql_server_nativ(self) -> bool:
        return self.system_type == self.sql_server_nativ_key

    @property
    def is_synapse_nativ(self) -> bool:
        return self.system_type == self.azure_synapse_key

    @property
    def is_db2_nativ(self) -> bool:
        return self.system_type == self.db2_key

    @property
    def is_postgres_sql_nativ(self) -> bool:
        return self.system_type == self.postgresql_key

    @property
    def is_azurepostgres_sql_nativ(self) -> bool:
        return self.system_type == self.azurepostgresql_key

    @property
    def is_oracle_db(self) -> bool:
        return self.system_type == self.oracle_key

    @property
    def is_azure_blob(self) -> bool:
        return self.system_type == self.azure_blob_key

    @property
    def is_tsql(self) -> bool:
        return (
            self.is_synapse_nativ or self.is_azure_sql_nativ or self.is_sql_server_nativ
        )

    def get_short_id(self) -> str:
        return str(self.id).split("-")[0]

    def get_object_identifier(self, schema_name: str, object_name: str) -> str:
        if self.system_type in (
            self.azure_synapse_key,
            self.azure_server_nativ_key,
            self.sql_server_nativ_key,
        ):
            ob_identifier = f"[{schema_name}].[{object_name}]"
        elif self.system_type in (
            self.snowflake_nativ_key,
            self.db2_key,
            self.postgresql_key,
            self.azurepostgresql_key,
        ):
            ob_identifier = f"{schema_name}.{object_name}"
        else:
            logger.error(
                "No object qualifier defined for system_type %s", self.system_type
            )
            raise NotImplementedError
        return ob_identifier

    def get_max_from_column(
        self,
        column_name: str,
        schema_name: str,
        object_name: str,
    ) -> str:
        """Creates query to retrieve the column max
        of a specified table.

        Args:
            column_name (str): _description_
            schema_name (str): _description_
            object_name (str): _description_
            catalog_name (str | None, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        object_identifier = self.get_object_identifier(
            schema_name=schema_name, object_name=object_name
        )
        return f'select max({column_name}) AS "max_value" from {object_identifier}'

    def get_procedure_call(self, proc_schema: str, proc_name: str) -> str:
        if self.system_type in (
            self.azure_synapse_key,
            self.azure_server_nativ_key,
            self.sql_server_nativ_key,
        ):
            template = env.get_template("mssql_procedure_call.sql.j2")
            query = template.render(
                procedure_identifier=self.get_object_identifier(proc_schema, proc_name),
                parameters={},
            )
            return query
        if self.system_type in (self.snowflake_nativ_key):
            template = env.get_template("snowsql_procedure_call.sql.j2")
            query = template.render(
                procedure_identifier=self.get_object_identifier(proc_schema, proc_name),
                parameters={},
            )
            return query
        logger.error(
            "No call stored procedure templates for system_type %s", self.system_type
        )
        raise NotImplementedError

    def get_procedure_call_with_parameters(
        self,
        proc_schema: str,
        proc_name: str,
        proc_parameters: dict[str, str],
        escape_quote_params: bool = True,
    ) -> str:
        quote_character = "''"
        if not escape_quote_params:
            quote_character = "'"
        if self.system_type in (
            self.azure_synapse_key,
            self.azure_server_nativ_key,
            self.sql_server_nativ_key,
        ):
            template = env.get_template("mssql_procedure_call.sql.j2")
            query = template.render(
                procedure_identifier=self.get_object_identifier(proc_schema, proc_name),
                parameters=proc_parameters,
                escape_character=quote_character,
            )
            return query
        if self.system_type in (self.snowflake_nativ_key):
            template = env.get_template("snowsql_procedure_call.sql.j2")
            query = template.render(
                procedure_identifier=self.get_object_identifier(proc_schema, proc_name),
                parameters=proc_parameters,
                escape_character=quote_character,
            )
            return query
        logger.error(
            "No call stored procedure with parameters templates for system_type %s",
            self.system_type,
        )
        raise NotImplementedError

    def get_procedure_create(
        self,
        proc_schema: str,
        proc_name: str,
        queries: list[str],
        is_transaction: bool = False,
    ) -> str:
        if self.system_type in (
            self.azure_synapse_key,
            self.azure_server_nativ_key,
            self.sql_server_nativ_key,
        ):
            template = env.get_template("mssql_procedure_create.sql.j2")
            query = template.render(
                procedure_identifier=self.get_object_identifier(proc_schema, proc_name),
                queries=queries,
            )
            return query
        if self.system_type in (self.snowflake_nativ_key):
            queries = [query.replace("\n", " ") for query in queries]
            template = env.get_template("snowsql_procedure_create.sql.j2")
            query = template.render(
                procedure_identifier=self.get_object_identifier(proc_schema, proc_name),
                queries=queries,
                is_transaction=is_transaction,
                parameters={},
            )
            return query
        logger.error(
            "No create stored procedure templates for system_type %s", self.system_type
        )
        raise NotImplementedError

    def get_query_postfix(self) -> str:
        if self.system_type in (
            self.azure_synapse_key,
            self.azure_server_nativ_key,
            self.sql_server_nativ_key,
        ):
            return "\n\nGO\n\n"
        if self.system_type in (self.snowflake_nativ_key):
            return "\n\n"
        logger.error("No query postfix templates for system_type %s", self.system_type)
        raise NotImplementedError
