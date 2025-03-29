from cloecore.to_datafactory.arm.datafactory import activities, linked_services


class ExecuteStoredProcedureViaScriptActivity(activities.ScriptActivity):
    """Resembles a adf script activity designed
    to call stored procedures. Should only be used
    in cases where regular stored procedure activity
    is not an option.
    """

    def __init__(
        self,
        name: str,
        linked_service: linked_services.SnowflakeLinkedService,
        stored_procedure_identifier: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(name, linked_service, description, act_depends_on)
        self.stored_procedure_identifier = stored_procedure_identifier

    def _create_call_query(self) -> str:
        call_prefix = ""
        call_postfix = ""
        parameters = []
        for _ in self.query_params.values():
            parameters.append("?")
        if len(parameters) > 0:
            return (
                f"{call_prefix}call {self.stored_procedure_identifier}"
                f"({', '.join(parameters)});{call_postfix}"
            )
        return f"{call_prefix}call {self.stored_procedure_identifier}();{call_postfix}"

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms the class to an ARM template
        snippet.

        Returns:
            dict: _description_
        """
        query = self._create_call_query()
        self.scripts.append(
            {
                "type": "Query",
                "text": query,
                "parameters": list(self.query_params.values()),
            }
        )
        base = super().to_arm()
        return base
