from cloecore.to_datafactory.arm.datafactory.activities import ForEachActivity
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity
from cloecore.to_datafactory.arm.datafactory.custom_activities import mssql, snowflake


class FS2DBForeach(ForEachActivity):
    def __init__(
        self,
        name: str,
        file_get_activity: mssql.MSSQLFileCatalogGetActivity
        | snowflake.SnowflakeRetrieveFilesFromBlobActivity
        | snowflake.SnowflakeFileCatalogGetActivity,
        is_sequential: bool | None = True,
        activities: list[BaseActivity] | None = None,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        self.file_get_activity = file_get_activity
        super().__init__(
            name,
            {},
            is_sequential,
            activities,
            description,
            act_depends_on,
            res_depends_on,
        )

    def to_arm(self) -> dict[str, dict | str | list]:
        file_get = self.file_get_activity
        self.items = file_get.get_script_activity_all_rows_return_expression()
        if isinstance(file_get, snowflake.SnowflakeRetrieveFilesFromBlobActivity):
            self.items = file_get.get_script_activity_snowflake_sp_return_expression(
                "RETRIEVE_FILES_FROM_BLOB"
            )
        if isinstance(file_get, mssql.MSSQLFileCatalogGetActivity):
            self.items = file_get.get_activity_output_parameter_array_expression()
        return super().to_arm()
