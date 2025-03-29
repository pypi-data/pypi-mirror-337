from cloecore.to_datafactory.arm.datafactory import activities, linked_services


class SnowflakeFileCatalogUpdateActivity(activities.ScriptActivity):
    """Resembles the activity to update the filecatalog after
    loading the file. Snowflake only and used for cases where
    files are retrieved from the filecatalog. Base activity,
    should not be used directly.
    """

    file_flag: int = 0

    def __init__(
        self,
        linked_service: linked_services.SnowflakeLinkedService,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name=self._get_act_name(),
            linked_service=linked_service,
            description=description,
            act_depends_on=act_depends_on,
        )
        self._create_parameter(
            name="catalog_file_id",
            value=self._get_pipeline_parameter_expression("catalog_file_id"),
            param_type="Int32",
        )

    def _get_act_name(self) -> str:
        if self.file_flag == 3:
            return "Set processed file Failure flag"
        return "Set processed file Success flag"

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms class to corresponding arm
        template snippet.

        Returns:
            dict: _description_
        """
        query = f"UPDATE cloe_dwh.FileCatalog SET filestatus = {self.file_flag}"
        if self.file_flag == 3:
            query += " , message = ''"
        query += " WHERE id = ?"
        self.scripts.append(
            {
                "type": "Query",
                "text": query,
                "parameters": list(self.query_params.values()),
            }
        )
        base = super().to_arm()
        return base


class SnowflakeFileCatalogUpdateSuccessActivity(SnowflakeFileCatalogUpdateActivity):
    """Resembles the activity to update the filecatalog after
    loading the file. Snowflake only and used for cases where
    files are retrieved from the filecatalog.  Builds on
    SnowflakeFileCatalogUpdateActivity and
    updates files as successful.
    """

    file_flag = 2


class SnowflakeFileCatalogUpdateFailureActivity(SnowflakeFileCatalogUpdateActivity):
    """Resembles the activity to update the filecatalog after
    loading the file. Snowflake only and used for cases where
    files are retrieved from the filecatalog.  Builds on
    SnowflakeFileCatalogUpdateActivity and
    updates files as failed.
    """

    file_flag = 3
