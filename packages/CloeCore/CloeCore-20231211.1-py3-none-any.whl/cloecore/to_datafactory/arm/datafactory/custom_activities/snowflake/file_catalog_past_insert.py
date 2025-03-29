from cloecore.to_datafactory.arm.datafactory import linked_services
from cloecore.to_datafactory.arm.datafactory.custom_activities.snowflake import (
    execute_stored_procedure_via_script,
)


class SnowflakeFileCatalogPastInsertActivity(
    execute_stored_procedure_via_script.ExecuteStoredProcedureViaScriptActivity
):
    """Resembles the script activity to insert new files into the filecatalog for cases
    where files are retrieved from blob first. Base activity, should not be used
    directly.
    """

    failed_flag: int = 0

    def __init__(
        self,
        linked_service: linked_services.SnowflakeLinkedService,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name=self._get_act_name(),
            linked_service=linked_service,
            stored_procedure_identifier="cloe_dwh.UPDATE_FILE_CATALOG",
            description=description,
            act_depends_on=act_depends_on,
        )
        self.pipeline_parameters.append("file_path")
        self._create_parameter(
            name="file_path",
            value=self._get_pipeline_parameter_expression("file_path"),
            param_type="String",
        )
        if self.failed_flag:
            self._create_parameter(name="message", value="Failed", param_type="String")
        else:
            self._create_parameter(name="message", value="Success", param_type="String")

    def _get_act_name(self) -> str:
        if self.failed_flag:
            return "Set processed file Failure flag"
        return "Set processed file Success flag"


class SnowflakeFileCatalogPastInsertSuccessActivity(
    SnowflakeFileCatalogPastInsertActivity
):
    """Resembles the script activity to insert new files into the filecatalog for cases
    where files are retrieved from blob first. Builds on
    SnowflakeFileCatalogPastInsertActivity and inserts new files as successful.
    """

    failed_flag = 0


class SnowflakeFileCatalogPastInsertFailureActivity(
    SnowflakeFileCatalogPastInsertActivity
):
    """Resembles the script activity to insert new files into the filecatalog for cases
    where files are retrieved from blob first. Builds on
    SnowflakeFileCatalogPastInsertActivity and inserts new files as failed.
    """

    failed_flag = 1
