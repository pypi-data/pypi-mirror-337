from cloecore.to_datafactory.arm.datafactory import activities


class SetVariableFileName(activities.SetVariableActivity):
    """Wrapper class for setting a adf variable that
    holds the filename for copy activity and filecatalog
    insert/update activity.
    """

    def __init__(
        self,
        ds_out_sink_file_template: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        variable_value = {
            "value": (
                f"@concat('{ds_out_sink_file_template}.', "
                "formatDateTime(utcNow(), 'yyyyMMddHHmmss'), '.parquet')"
            ),
            "type": "Expression",
        }
        super().__init__(
            name="Set filename",
            variable_value=variable_value,
            description=description,
            act_depends_on=act_depends_on,
            res_depends_on=res_depends_on,
        )
