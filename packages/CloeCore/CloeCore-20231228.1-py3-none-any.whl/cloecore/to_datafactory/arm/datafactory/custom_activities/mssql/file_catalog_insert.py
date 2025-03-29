from cloecore.to_datafactory.arm.datafactory import activities, linked_services
from cloecore.to_datafactory.arm.datafactory.custom_activities import (
    delta_get_end_sequence,
)


class MSSQLFileCatalogInsertActivity(activities.ExecuteStoredProcedureActivity):
    """Wrapper activity for ExecuteStoredProcedureActivity activity. Insert files
    into filecatalog using a stored procedure. MSSQL Only.
    """

    def __init__(
        self,
        linked_service: linked_services.AzureSqlLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService,
        ds_out_sink_directory: str,
        datasource_info_id: str,
        datasttype_id: str,
        filestorage_id: str,
        sink_file_name_variable: activities.SetVariableActivity,
        delta_end_sequence: delta_get_end_sequence.DeltaGetEndSequence | None = None,
        sequence_column_name: str | None = None,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name="Add file to file queue",
            linked_service=linked_service,
            stored_procedure_identifier="cloe_dwh.spInsertFileIntoFileCatalog",
            description=description,
            act_depends_on=act_depends_on,
        )
        self._create_parameter(
            name="pFilePath", value=ds_out_sink_directory, param_type="String"
        )
        self.file_name_variable = sink_file_name_variable
        self._create_parameter(
            name="pDatasourceInfo_ID", value=datasource_info_id, param_type="Guid"
        )
        self._create_parameter(
            name="pDatasetType_ID", value=datasttype_id, param_type="Guid"
        )
        self._create_parameter(
            name="pFileStorage_ID", value=filestorage_id, param_type="Guid"
        )
        self._delta_end_sequence = delta_end_sequence
        self._sequence_column_name = sequence_column_name

    def _initalize_sequence_handling(
        self,
        delta_end_sequence: delta_get_end_sequence.DeltaGetEndSequence | None = None,
        sequence_column_name: str | None = None,
    ) -> None:
        if delta_end_sequence is None or sequence_column_name is None:
            self._create_parameter(
                name="pSequenceColumnName", value="", param_type="String"
            )
            self._create_parameter(name="pLastSequence", value="", param_type="String")
        else:
            self._create_parameter(
                name="pSequenceColumnName",
                value=sequence_column_name,
                param_type="String",
            )
            act_get_seq_end_out = delta_end_sequence.get_lookup_first_row_first_col(
                column_index_name="max_value"
            )
            self._create_parameter(
                name="pLastSequence", value=act_get_seq_end_out, param_type="String"
            )

    def to_arm(self) -> dict[str, dict | str | list]:
        self._create_parameter(
            name="pFileName",
            value=self._get_variable_expression(self.file_name_variable.variable_name),
            param_type="String",
        )
        self._initalize_sequence_handling(
            self._delta_end_sequence, self._sequence_column_name
        )
        return super().to_arm()
