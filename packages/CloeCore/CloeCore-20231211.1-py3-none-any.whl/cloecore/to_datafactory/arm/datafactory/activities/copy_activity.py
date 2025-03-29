from cloecore.to_datafactory.arm.datafactory import datasets
from cloecore.to_datafactory.arm.datafactory.activities import support
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity


class CopyActivity(BaseActivity):
    """CopyActivity bass class resembling
    a copy activity in ADF.
    """

    def __init__(
        self,
        name: str,
        source_ds: datasets.AzureSqlDataset
        | datasets.AzureSynapseAnalyticsDataset
        | datasets.SqlServerDataset
        | datasets.SnowflakeDataset
        | datasets.OracleDataset
        | datasets.DB2Dataset
        | datasets.PostgreSQLDataset
        | datasets.AzurePostgreSQLDataset
        | datasets.ParquetDataset,
        sink_ds: datasets.AzureSqlDataset
        | datasets.AzureSynapseAnalyticsDataset
        | datasets.ParquetDataset,
        source_values: dict[str, str | dict[str, str]] | None = None,
        sink_values: dict[str, str | dict[str, str]] | None = None,
        source_sql_reader_query: dict[str, str] | str | None = None,
        pre_insert_query: str | None = None,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(name, description, act_depends_on, res_depends_on)
        self.source_ds = source_ds
        self.source_values = source_values
        self.sink_ds = sink_ds
        self.sink_values = sink_values
        self.reader_query = source_sql_reader_query
        self.pre_insert_query = pre_insert_query

    def _get_source(self) -> dict:
        if isinstance(self.source_ds, datasets.ParquetDataset):
            return support.ParquetSource().to_arm()
        if isinstance(self.source_ds, datasets.AzureSqlDataset):
            return support.AzureSqlSource(self.reader_query).to_arm()
        if isinstance(self.source_ds, datasets.AzureSynapseAnalyticsDataset):
            return support.AzureSynapseAnalyticsSource(self.reader_query).to_arm()
        if isinstance(self.source_ds, datasets.SnowflakeDataset):
            return support.SnowflakeSource(self.reader_query).to_arm()
        if isinstance(self.source_ds, datasets.OracleDataset):
            return support.OracleSource(self.reader_query).to_arm()
        if isinstance(self.source_ds, datasets.SqlServerDataset):
            return support.SqlServerSqlSource(self.reader_query).to_arm()
        if isinstance(self.source_ds, datasets.DB2Dataset):
            return support.DB2Source(self.reader_query).to_arm()
        if isinstance(self.source_ds, datasets.PostgreSQLDataset):
            return support.PostgreSQLSource(self.reader_query).to_arm()
        if isinstance(self.source_ds, datasets.AzurePostgreSQLDataset):
            return support.AzurePostgreSQLSource(self.reader_query).to_arm()

    def _get_sink(self) -> dict:
        if isinstance(self.sink_ds, datasets.ParquetDataset):
            return support.ParquetSink().to_arm()
        if isinstance(self.sink_ds, datasets.AzureSqlDataset):
            return support.AzureSqlSink(self.pre_insert_query).to_arm()
        if isinstance(self.sink_ds, datasets.AzureSynapseAnalyticsDataset):
            return support.AzureSynapseAnalyticsSink(self.pre_insert_query).to_arm()

    def get_res_deps_of(self) -> list:
        """Get ARM dependencies of
        datasets and then calls parent method.

        Returns:
            list: _description_
        """
        self.res_depends_on += (
            self.source_ds.get_dependency_on() + self.sink_ds.get_dependency_on()
        )
        return super().get_res_deps_of()

    def _to_arm(self) -> dict:
        return {
            "type": "Copy",
            "policy": {
                "timeout": "7.00:00:00",
                "retry": 0,
                "retryIntervalInSeconds": 30,
                "secureOutput": False,
                "secureInput": False,
            },
            "typeProperties": {
                "source": self._get_source(),
                "sink": self._get_sink(),
                "enableStaging": False,
            },
            "inputs": [self.source_ds.get_reference(self.source_values)],
            "outputs": [self.sink_ds.get_reference(self.sink_values)],
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms the class to ARM template
        snippet.

        Returns:
            dict: _description_
        """
        base = super().to_arm()
        base |= self._to_arm()
        return base
