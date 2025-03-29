from cloecore.to_datafactory.arm.datafactory.datasets.base import DatasetResource
from cloecore.to_datafactory.arm.datafactory.linked_services import base


class TableDataset(DatasetResource):
    """Wrapper class for DatasetResource. Intermediate class
    for creating datasets
    for systems that require a schema and table name.
    """

    db_type: str = "Default"

    def __init__(
        self,
        name: str,
        linked_service: base.LinkedServiceBase,
        folder_name: str,
        annotations: list[str] | None = None,
        schema: list | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name,
            linked_service,
            folder_name,
            annotations,
            schema,
            required_arm_variables,
        )
        self._create_parameter(name="schemaName")
        self._create_parameter(name="tableName")

    def _to_arm(self) -> dict:
        return {
            "type": self.db_type,
            "typeProperties": {
                "schema": self._get_parameter_expression("schemaName"),
                "table": self._get_parameter_expression("tableName"),
            },
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms the class to ARM template
        snippet.

        Returns:
            dict: _description_
        """
        self.properties = self._to_arm()
        return super().to_arm()


class AzureSqlDataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for Azure Sql.
    """

    db_type = "AzureSqlTable"


class AzureSynapseAnalyticsDataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for Azure Synapse.
    """

    db_type = "AzureSQLDWDataset"


class OracleDataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for Oracle.
    """

    db_type = "OracleTable"


class SnowflakeDataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for Snowflake.
    """

    db_type = "SnowflakeTable"


class SqlServerDataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for SqlServer.
    """

    db_type = "SqlServerTable"


class DB2Dataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for DB2.
    """

    db_type = "DB2Table"


class PostgreSQLDataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for DB2.
    """

    db_type = "PostgreSqlTable"


class AzurePostgreSQLDataset(TableDataset):
    """Wrapper class for TableDataset.
    Initializing a TableDataset for DB2.
    """

    db_type = "AzurePostgreSqlTable"
