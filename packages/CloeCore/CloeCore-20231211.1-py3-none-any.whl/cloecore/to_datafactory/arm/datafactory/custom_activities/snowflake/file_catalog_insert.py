from cloecore.to_datafactory.arm.datafactory import activities, linked_services
from cloecore.to_datafactory.arm.datafactory.custom_activities import (
    delta_get_end_sequence,
)


class SnowflakeFileCatalogInsertActivity(activities.ScriptActivity):
    """Wrapper class to create a script activity to insert
    a new file into the FileCatalog.

    Args:
        ScriptActivity (_type_): _description_
    """

    def __init__(
        self,
        ds_out_sink_directory: str,
        datasource_info_id: str,
        datasttype_id: str,
        filestorage_id: str,
        sink_file_name_variable: activities.SetVariableActivity,
        linked_service: linked_services.SnowflakeLinkedService,
        delta_end_sequence: delta_get_end_sequence.DeltaGetEndSequence | None = None,
        sequence_column_name: str | None = None,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name="Add file to FileCatalog",
            linked_service=linked_service,
            description=description,
            act_depends_on=act_depends_on,
        )
        self.ds_out_sink_directory = ds_out_sink_directory
        self.datasource_info_id = datasource_info_id
        self.datasttype_id = datasttype_id
        self.filestorage_id = filestorage_id
        self.sequence_column_name = sequence_column_name
        self._create_parameter(
            name="file_path", value=ds_out_sink_directory, param_type="String"
        )
        self.file_name_variable = sink_file_name_variable
        self._create_parameter(
            name="fk_datasourceinfo_id", value=datasource_info_id, param_type="String"
        )
        self._create_parameter(
            name="fk_datasettype_id", value=datasttype_id, param_type="String"
        )
        self._create_parameter(
            name="fk_cn_filestorage_id", value=filestorage_id, param_type="String"
        )
        self._delta_end_sequence = delta_end_sequence
        self._sequence_column_name = sequence_column_name

    def _initalize_sequence_handling(
        self,
        delta_end_sequence: delta_get_end_sequence.DeltaGetEndSequence | None = None,
        sequence_column_name: str | None = None,
    ) -> None:
        if delta_end_sequence is not None and sequence_column_name is not None:
            self._create_parameter(
                name="sequencecolumnname",
                value=sequence_column_name,
                param_type="String",
            )
            act_get_seq_end_out = delta_end_sequence.get_lookup_first_row_first_col(
                column_index_name="max_value"
            )
            self._create_parameter(
                name="lastsequence", value=act_get_seq_end_out, param_type="String"
            )

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms class to corresponding arm
        template snippet.

        Returns:
            dict: _description_
        """
        self._initalize_sequence_handling(
            self._delta_end_sequence, self._sequence_column_name
        )
        query = (
            "INSERT INTO cloe_dwh.FileCatalog(filepath,"
            " fk_datasourceinfo_id, fk_datasettype_id, fk_cn_filestorage_id,"
            " sequencecolumnname, lastsequence, filename) VALUES "
        )
        if self.sequence_column_name is None:
            query += "(?, ?, ?, ?, NULL, NULL, ?);"
        else:
            query += "(?, ?, ?, ?, ?, ?, ?);"
        self._create_parameter(
            name="file_name",
            value=self._get_variable_expression(self.file_name_variable.variable_name),
            param_type="String",
        )
        self.scripts.append(
            {
                "type": "Query",
                "text": query,
                "parameters": list(self.query_params.values()),
            }
        )
        base = super().to_arm()
        return base
