from cloecore.to_datafactory.arm.datafactory import activities, datasets
from cloecore.to_datafactory.arm.datafactory.custom_activities import (
    delta_get_end_sequence,
)
from cloecore.to_datafactory.arm.datafactory.custom_activities.snowflake import (
    delta_get_start_sequence,
)


class DB2FSCopyActivity(activities.CopyActivity):
    """CopyActivity specific to DB2FS jobs. Builds
    on CopyActivity class.
    """

    def __init__(
        self,
        source_ds: datasets.AzureSqlDataset
        | datasets.AzureSynapseAnalyticsDataset
        | datasets.SqlServerDataset
        | datasets.SnowflakeDataset
        | datasets.OracleDataset
        | datasets.DB2Dataset
        | datasets.PostgreSQLDataset
        | datasets.AzurePostgreSQLDataset,
        sink_ds: datasets.ParquetDataset,
        source_schema_name: str,
        source_table_name: str,
        source_sql_reader_query: str,
        sink_file_path: str,
        sink_file_name_variable: activities.SetVariableActivity,
        delta_start_sequence: delta_get_start_sequence.DeltaGetStartSequence
        | None = None,
        delta_end_sequence: delta_get_end_sequence.DeltaGetEndSequence | None = None,
        sequence_column_name: str | None = None,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(
            name="Copy to FS",
            source_ds=source_ds,
            sink_ds=sink_ds,
            source_values={
                "schemaName": source_schema_name,
                "tableName": source_table_name,
            },
            source_sql_reader_query=source_sql_reader_query,
            description=description,
            act_depends_on=act_depends_on,
            res_depends_on=res_depends_on,
        )
        self.file_name_variable = sink_file_name_variable
        self.sink_values = {
            "folderPath": sink_file_path,
            "fileName": {},
        }
        self._delta_end_sequence = delta_end_sequence
        self._delta_start_sequence = delta_start_sequence
        self._sequence_column_name = sequence_column_name
        self._reader_query = source_sql_reader_query

    def get_delta_start_end(
        self,
        query: str,
        query_end_snippet,
        start_input: delta_get_end_sequence.DeltaGetEndSequence,
        end_input: delta_get_start_sequence.DeltaGetStartSequence,
    ) -> dict[str, str]:
        """Combines multiple methods to create the copy activity
        delta extraction expression.

        Args:
            query (str): _description_
            query_end_snippet (_type_): _description_
            start_input (str): _description_
            end_input_check (str): _description_
            end_input_expression (str): _description_

        Returns:
            str: _description_
        """
        start_input_value = start_input._lookup_first_row_output(
            column_index="max_value"
        )
        end_input_check = end_input._script_activity_resultset_return_expression()
        end_input_expression = end_input._script_activity_resultset_return_expression(
            resultsets_index=0, rows_index=0, row_selector="LASTSEQUENCE"
        )
        save_query = query.replace("'", "''")
        expression = self._replace_string_expression(
            self._replace_string_expression(
                f"'{save_query}'",
                "'$SEQUENCE_END'",
                self._convert_to_string_expression(start_input_value),
            ),
            "'$SEQUENCE_START'",
            self._convert_to_string_expression(
                self._if_expression(
                    self._less_or_equals_expression(
                        self._length_expression(end_input_check), 0
                    ),
                    "''",
                    self._concat_expression(
                        [
                            {"type": "s", "value": f"{query_end_snippet} '"},
                            {"type": "e", "value": end_input_expression},
                            {"type": "s", "value": "'"},
                        ]
                    ),
                )
            ),
        )
        return {
            "value": f"@{expression}",
            "type": "Expression",
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms the class to ARM template
        snippet.

        Returns:
            dict: _description_
        """
        if (
            self._delta_end_sequence is not None
            and self._delta_start_sequence is not None
        ):
            self.reader_query = self.get_delta_start_end(
                self._reader_query,
                f"and {self._sequence_column_name} >=",
                self._delta_end_sequence,
                self._delta_start_sequence,
            )
        if self.sink_values is not None:
            self.sink_values["fileName"] = self._get_variable_expression(
                self.file_name_variable.variable_name
            )
        return super().to_arm()
