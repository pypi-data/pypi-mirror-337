from cloecore.to_datafactory.arm.datafactory import activities, datasets


class FS2DBCopyActivity(activities.CopyActivity):
    """CopyActivity specific to FS2DB jobs. Builds
    on CopyActivity class.
    """

    def __init__(
        self,
        source_ds: datasets.ParquetDataset,
        sink_ds: datasets.AzureSqlDataset | datasets.AzureSynapseAnalyticsDataset,
        sink_table_identifier: str,
        sink_schema_name: str,
        sink_table_name: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(
            name="Copy to DB",
            source_ds=source_ds,
            sink_ds=sink_ds,
            sink_values={"schemaName": sink_schema_name, "tableName": sink_table_name},
            pre_insert_query=f"TRUNCATE TABLE {sink_table_identifier};",
            description=description,
            act_depends_on=act_depends_on,
            res_depends_on=res_depends_on,
        )
        self.sink_schema_name = sink_schema_name
        self.sink_table_name = sink_table_name
        self.sink_table_identifier: str = sink_table_identifier
        self.source_values = {
            "folderPath": self._get_pipeline_parameter_expression("folder_path"),
            "fileName": self._get_pipeline_parameter_expression("file_name"),
        }
