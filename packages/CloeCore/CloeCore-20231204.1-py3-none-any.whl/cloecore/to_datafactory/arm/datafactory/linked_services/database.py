import cloecore.to_datafactory.arm.general.parameter as param
from cloecore.to_datafactory.arm.datafactory.linked_services import base
from cloecore.utils.model.jobs.connections import Connection


class DatabaseLinkedService(base.LinkedServiceBase):
    """Wrapper class for LinkedServiceBase. Intermediate class
    for creating LinkedServices for database systems.
    """

    property_type: str = "Default"

    def __init__(
        self,
        name: str,
        connection: Connection,
        secret_reference: dict,
        depends_on: list | None = None,
        required_arm_parameters: dict[str, dict] | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name,
            connection,
            depends_on,
            required_arm_parameters,
            required_arm_variables,
        )
        self.connection_string = secret_reference
        self.annotations: list[str] = []
        self.required_arm_parameters |= param.Parameter(
            f"ConnectVia{name}", default_value="null"
        ).get_reference()

    def _to_arm(self) -> dict:
        connect_via = (
            f"[if(equals(parameters('ConnectVia{self.name}'), 'null'),"
            f" null(), createObject('referenceName', parameters('ConnectVia{self.name}'"
            "), 'type', 'IntegrationRuntimeReference'))]"
        )
        return {
            "type": self.property_type,
            "typeProperties": {"connectionString": self.connection_string},
            "connectVia": connect_via,
            "annotations": self.annotations,
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms the class to ARM template
        snippet.

        Returns:
            dict: _description_
        """
        self.properties = self._to_arm()
        return super().to_arm()


class AzureSqlLinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for Azure SQL.
    """

    property_type = "AzureSqlDatabase"


class AzureSynapseAnalyticsLinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for Azure Synapse.
    """

    property_type = "AzureSqlDW"


class OracleLinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for Oracle.
    """

    property_type = "Oracle"


class SnowflakeLinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for Snowflake.
    """

    property_type = "Snowflake"


class SqlServerLinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for SqlServer.
    """

    property_type = "SqlServer"


class DB2LinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for DB2.
    """

    property_type = "Db2"


class PostgreSQLLinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for DB2.
    """

    property_type = "PostgreSql"


class AzurePostgreSQLLinkedService(DatabaseLinkedService):
    """Wrapper class for DatabaseLinkedService.
    Initializing a LinkedService for DB2.
    """

    property_type = "AzurePostgreSql"
