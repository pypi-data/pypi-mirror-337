from typing import Union

from cloecore.to_datafactory.arm.datafactory import activities, datasets
from cloecore.to_datafactory.arm.datafactory.activities import support


def get_source_properties(
    source_ds: datasets.AzureSqlDataset
    | datasets.AzureSynapseAnalyticsDataset
    | datasets.DB2Dataset
    | datasets.OracleDataset
    | datasets.SqlServerDataset
    | datasets.SnowflakeDataset
    | datasets.PostgreSQLDataset
    | datasets.AzurePostgreSQLDataset,
    query: str,
) -> Union[
    support.AzureSqlSource,
    support.AzureSqlSource,
    support.DB2Source,
    support.OracleSource,
    support.SqlServerSqlSource,
    support.SnowflakeSource,
    support.PostgreSQLSource,
    support.AzurePostgreSQLSource,
]:
    if isinstance(source_ds, datasets.AzureSqlDataset):
        return support.AzureSqlSource(query)
    if isinstance(source_ds, datasets.AzureSynapseAnalyticsDataset):
        return support.AzureSqlSource(query)
    if isinstance(source_ds, datasets.DB2Dataset):
        return support.DB2Source(query)
    if isinstance(source_ds, datasets.OracleDataset):
        return support.OracleSource(query)
    if isinstance(source_ds, datasets.SqlServerDataset):
        return support.SqlServerSqlSource(query)
    if isinstance(source_ds, datasets.SnowflakeDataset):
        return support.SnowflakeSource(query)
    if isinstance(source_ds, datasets.PostgreSQLDataset):
        return support.PostgreSQLSource(query)
    if isinstance(source_ds, datasets.AzurePostgreSQLDataset):
        return support.AzurePostgreSQLSource(query)


class DeltaGetEndSequence(activities.LookupActivity):
    """Wrapper class for LookupActivity. Resembles
    a lookup to retrieve delta end sequence.
    """

    def __init__(
        self,
        source_ds: datasets.AzureSqlDataset
        | datasets.AzureSynapseAnalyticsDataset
        | datasets.DB2Dataset
        | datasets.OracleDataset
        | datasets.SqlServerDataset
        | datasets.SnowflakeDataset
        | datasets.PostgreSQLDataset
        | datasets.AzurePostgreSQLDataset,
        schema_name: str,
        table_name: str,
        sequence_column_name: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        self.query = source_ds.linked_service.connection.get_max_from_column(
            column_name=sequence_column_name,
            schema_name=schema_name,
            object_name=table_name,
        )
        self.sequence_column_name = sequence_column_name
        source_properties = get_source_properties(source_ds, self.query)
        super().__init__(
            name="Get end sequence",
            source_ds=source_ds,
            source_properties=source_properties,
            ds_params={"schemaName": schema_name, "tableName": table_name},
            first_row_only=True,
            description=description,
            act_depends_on=act_depends_on,
            res_depends_on=res_depends_on,
        )
