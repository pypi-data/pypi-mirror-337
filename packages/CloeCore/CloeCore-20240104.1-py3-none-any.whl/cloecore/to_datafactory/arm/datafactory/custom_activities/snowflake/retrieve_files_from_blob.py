from cloecore.to_datafactory.arm.datafactory import linked_services
from cloecore.to_datafactory.arm.datafactory.custom_activities.snowflake import (
    execute_stored_procedure_via_script,
)


class SnowflakeRetrieveFilesFromBlobActivity(
    execute_stored_procedure_via_script.ExecuteStoredProcedureViaScriptActivity
):
    """Resembles an ADF script activity to call a procedure in
    Snowflake that retrieves and returns a list of files from
    the blob.
    """

    def __init__(
        self,
        linked_service: linked_services.SnowflakeLinkedService,
        file_path_pattern: str,
        file_name_pattern: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name="Retrieve files from blob",
            linked_service=linked_service,
            stored_procedure_identifier="cloe_dwh.RETRIEVE_FILES_FROM_BLOB",
            description=description,
            act_depends_on=act_depends_on,
        )
        if file_path_pattern is None:
            self._create_parameter(
                name="file_filter",
                value=f"{file_name_pattern}",
                param_type="String",
            )
        else:
            self._create_parameter(
                name="file_filter",
                value=f"{file_path_pattern}/{file_name_pattern}",
                param_type="String",
            )
