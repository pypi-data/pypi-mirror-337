from cloecore.to_datafactory.arm.datafactory import activities, linked_services


class DeltaGetStartSequence(activities.ScriptActivity):
    """Resembles the script activity to retrieve the latest
    sequence of a succesfully loaded file.
    """

    def __init__(
        self,
        linked_service: linked_services.SnowflakeLinkedService,
        datasource_info_id: str,
        datasttype_id: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name="Get start sequence",
            linked_service=linked_service,
            description=description,
            act_depends_on=act_depends_on,
        )
        self._create_parameter(
            name="datasource_info_id", value=datasource_info_id, param_type="String"
        )
        self._create_parameter(
            name="dataset_type_id", value=datasttype_id, param_type="String"
        )

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms class to corresponding arm
        template snippet.

        Returns:
            dict: _description_
        """
        query = (
            "select LASTSEQUENCE from cloe_dwh.FileCatalog where"
            " fk_datasourceinfo_id like ? and fk_datasettype_id like ? and"
            " filestatus = 2 and LASTSEQUENCE is not null order by id desc limit 1;"
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
