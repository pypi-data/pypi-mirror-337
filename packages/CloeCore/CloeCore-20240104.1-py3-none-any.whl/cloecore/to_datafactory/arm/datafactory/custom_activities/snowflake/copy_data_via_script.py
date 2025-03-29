from cloecore.to_datafactory.arm.datafactory import activities, linked_services
from cloecore.utils import model


class CopyDataViaScriptActivity(activities.ScriptActivity):
    """Resembles an ADF script activity to
    copy data into Snowflake.
    """

    def __init__(
        self,
        name: str,
        linked_service: linked_services.SnowflakeLinkedService,
        source_ls_name: str,
        table_identifier: str,
        get_from_filecatalog: bool,
        ds_type: model.DatasetType,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(name, linked_service, description, act_depends_on)
        self.ds_type = ds_type
        self.get_from_filecatalog = get_from_filecatalog
        self.scripts.append(
            {"type": "NonQuery", "text": f"TRUNCATE TABLE {table_identifier};"}
        )
        self.additional_options = self._infer_copy_additional_options()
        script_text_value = self._filecatalog_handling(source_ls_name, table_identifier)
        self.scripts.append(
            {
                "type": "NonQuery",
                "text": {"value": script_text_value, "type": "Expression"},
            }
        )

    def _filecatalog_handling(self, source_ls_name: str, table_identifier: str) -> str:
        if self.get_from_filecatalog:
            self.pipeline_parameters.append("folder_path")
            self.pipeline_parameters.append("file_name")
            self.pipeline_parameters.append("catalog_file_id")
            return (
                f"@concat('COPY INTO {table_identifier} FROM"
                f" @cloe_dwh.{source_ls_name}/', pipeline().parameters.folder_path,"
                f" '/', pipeline().parameters.file_name, ' {self.additional_options}"
                f" file_format = (format_name = cloe_dwh.{self.ds_type.name});')"
            )
        self.pipeline_parameters.append("file_path")
        return (
            f"@concat('COPY INTO {table_identifier} FROM"
            f" @cloe_dwh.{source_ls_name}/', pipeline().parameters.file_path,"
            f" ' {self.additional_options}"
            f" file_format = (format_name = cloe_dwh.{self.ds_type.name});')"
        )

    def _infer_copy_additional_options(self) -> str:
        additional_options = ""
        if self.ds_type.is_parquet:
            additional_options += "MATCH_BY_COLUMN_NAME = ''CASE_INSENSITIVE''"
        return additional_options
