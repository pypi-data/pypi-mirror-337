from cloecore.to_datafactory.arm.datafactory import activities, linked_services


class MSSQLFileCatalogUpdateActivity(activities.ExecuteStoredProcedureActivity):
    """Wrapper activity for ExecuteStoredProcedureActivity activity. Updates files
    in the filecatalog. MSSQL Only.
    """

    failed_flag: bool = False

    def __init__(
        self,
        linked_service: linked_services.AzureSqlLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name=self._get_act_name(),
            linked_service=linked_service,
            stored_procedure_identifier="cloe_dwh.spUpdateFileCatalog",
            description=description,
            act_depends_on=act_depends_on,
        )
        self._create_parameter(
            name="pFileLoadFailed", value=self.failed_flag, param_type="Boolean"
        )
        catalog_file_id_expression = self._get_pipeline_parameter_expression(
            "catalog_file_id"
        )
        self._create_parameter(
            name="pFilecatalogID", value=catalog_file_id_expression, param_type="Int32"
        )

    def _get_act_name(self) -> str:
        if self.failed_flag:
            return "Set processed file Failure flag"
        return "Set processed file Success flag"


class MSSQLFileCatalogUpdateSuccessActivity(MSSQLFileCatalogUpdateActivity):
    failed_flag = False


class MSSQLFileCatalogUpdateFailureActivity(MSSQLFileCatalogUpdateActivity):
    failed_flag = True
