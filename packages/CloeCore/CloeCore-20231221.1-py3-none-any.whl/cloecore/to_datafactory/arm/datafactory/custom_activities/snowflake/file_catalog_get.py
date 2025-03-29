from cloecore.to_datafactory.arm.datafactory import activities, linked_services


class SnowflakeFileCatalogGetActivity(activities.ScriptActivity):
    """Resembes the script activity to retrieve files
    from the filecatalog. Snowflake only.
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
            name="Retrieve pending files",
            linked_service=linked_service,
            description=description,
            act_depends_on=act_depends_on,
        )
        self._create_parameter(
            name="pLockGuid",
            value={"value": "@guid()", "type": "Expression"},
            param_type="String",
        )
        self._create_parameter(
            name="pFilepathPattern", value=file_path_pattern, param_type="String"
        )
        self._create_parameter(
            name="pFilenamePattern", value=file_name_pattern, param_type="String"
        )

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms class to corresponding arm
        template snippet.

        Returns:
            dict: _description_
        """
        query = (
            "set lock_uuid = ?; UPDATE cloe_dwh.FileCatalog SET filestatus = 1,"
            " lock_uuid = $lock_uuid WHERE filestatus = 0 and FilePath LIKE ? AND"
            " FileName LIKE ?; SELECT id, filepath, filename, fileparts from"
            " cloe_dwh.FileCatalog where filestatus = 1 and lock_uuid = $lock_uuid;"
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
