from cloecore.to_datafactory.arm.datafactory import activities, datasets
from cloecore.to_datafactory.arm.datafactory.activities import support


def get_source_properties(
    stored_procedure_query: str,
    source_ds: datasets.AzureSqlDataset | datasets.AzureSynapseAnalyticsDataset,
) -> support.AzureSynapseAnalyticsSource | support.AzureSqlSource:
    if isinstance(source_ds, datasets.AzureSynapseAnalyticsDataset):
        return support.AzureSynapseAnalyticsSource(stored_procedure_query)
    return support.AzureSqlSource(stored_procedure_query)


class MSSQLFileCatalogGetActivity(activities.LookupActivity):
    """Wrapper activity for Lookup activity. Retireves files
    from filecatalog. MSSQL Only.
    """

    def __init__(
        self,
        source_ds: datasets.AzureSqlDataset | datasets.AzureSynapseAnalyticsDataset,
        file_path_pattern: str,
        file_name_pattern: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        proc_parameters = {}
        proc_parameters["pFilepathPattern"] = file_path_pattern
        proc_parameters["pFilenamePattern"] = file_name_pattern
        self.stored_procedure_query = (
            source_ds.linked_service.connection.get_procedure_call_with_parameters(
                proc_schema="cloe_dwh",
                proc_name="spGetFilesFromFileCatalog",
                proc_parameters=proc_parameters,
                escape_quote_params=False,
            )
        )
        source_properties = get_source_properties(
            self.stored_procedure_query, source_ds
        )
        super().__init__(
            name="Retrieve pending files",
            source_ds=source_ds,
            source_properties=source_properties,
            ds_params={"schemaName": "cloe_dwh", "tableName": "FileCatalog"},
            first_row_only=False,
            description=description,
            act_depends_on=act_depends_on,
            res_depends_on=res_depends_on,
        )
