import logging

logger = logging.getLogger(__name__)


class SqlSource:
    """Base class for CopyActivity
    sources which are using an SQL sources.
    """

    sql_type: str = "Default"
    arm_sql_query_key = "sqlReaderQuery"

    def __init__(
        self,
        sql_query: dict[str, str] | str | None = None,
        additional_columns: list | None = None,
    ) -> None:
        self.ad_columns = additional_columns or []
        self.sql_query = sql_query

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms the class to ARM template
        snippet.

        Returns:
            dict: _description_
        """
        base: dict[str, dict | str | list] = {
            "type": self.sql_type,
            "additionalColumns": self.ad_columns,
            "queryTimeout": "02:00:00",
            "partitionOption": "None",
        }
        if self.sql_query is not None:
            base[self.arm_sql_query_key] = self.sql_query
        return base


class SqlServerSqlSource(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for SQL Server.
    """

    sql_type = "SqlSource"


class AzureSqlSource(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for Azure SQL.
    """

    sql_type = "AzureSqlSource"


class AzureSynapseAnalyticsSource(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for Azure Synapse.
    """

    sql_type = "SqlDWSource"


class OracleSource(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for Oracle.
    """

    sql_type = "OracleSource"
    arm_sql_query_key = "oracleReaderQuery"


class DB2Source(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for DB2.
    """

    sql_type = "Db2Source"
    arm_sql_query_key = "query"


class SnowflakeSource(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for Snowflake.
    """

    sql_type = "SnowflakeSource"

    def to_arm(self) -> dict[str, dict | str | list]:
        base = super().to_arm()
        if self.sql_query is not None:
            base["sqlReaderQuery"] = self.sql_query
        base["exportSettings"] = {
            "type": "SnowflakeExportCopyCommand",
            "additionalCopyOptions": {"MAX_FILE_SIZE": "64000000", "OVERWRITE": True},
            "additionalFormatOptions": {"DATE_FORMAT": "YYYY-MM-DD"},
        }
        return base


class PostgreSQLSource(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for DB2.
    """

    sql_type = "PostgreSqlSource"
    arm_sql_query_key = "query"


class AzurePostgreSQLSource(SqlSource):
    """Wrapper class for SqlSource.
    Initializing a copy activity SqlSource for DB2.
    """

    sql_type = "AzurePostgreSQLSource"
    arm_sql_query_key = "query"


class BlobSource:
    """Base class for CopyActivity
    sources which are using an blob sources.
    """

    store_type: str = "AzureBlobStorageReadSettings"
    file_type: str = "Default"

    def to_arm(self) -> dict[str, dict | str | list]:
        return {
            "type": self.file_type,
            "storeSettings": {"type": self.store_type, "recursive": True},
        }


class ParquetSource(BlobSource):
    """Wrapper class for BlobSource.
    Initializing a copy activity BlobSource for Parquet.
    """

    file_type = "ParquetSource"
