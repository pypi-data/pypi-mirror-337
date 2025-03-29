from cloecore.to_datafactory.arm.datafactory import activities, pipeline_resource


class MSSQLProcessFilesExecutePipelineActivity(activities.ExecutePipelineActivity):
    """Wrapper activity for ExecuteStoredProcedureActivity activity. Updates files
    in the filecatalog. MSSQL Only.
    """

    def __init__(
        self,
        name: str,
        pipeline: pipeline_resource.PipelineResource,
        foreach: activities.ForEachActivity,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(
            name,
            pipeline,
            wait_on_completion=True,
            description=description,
            act_depends_on=act_depends_on,
            res_depends_on=res_depends_on,
        )
        self._create_parameter(
            name="folder_path", value=foreach.get_item_expression("FilePath")
        )
        self._create_parameter(
            name="file_name", value=foreach.get_item_expression("FileName")
        )
        self._create_parameter(
            name="catalog_file_id", value=foreach.get_item_expression("ID")
        )
