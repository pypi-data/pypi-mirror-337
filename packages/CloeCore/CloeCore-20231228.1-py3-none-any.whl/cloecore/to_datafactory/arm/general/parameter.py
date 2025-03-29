class Parameter:
    """Basic class for ARM template parameters."""

    def __init__(
        self,
        name: str,
        param_type: str = "string",
        default_value: str | dict | None = None,
    ) -> None:
        self.name = name
        self.param_type = param_type
        self.default_value = default_value

    def get_standalone(self) -> str:
        return f"[parameters('{self.name}')]"

    def get_expression(self) -> str:
        return f"parameters('{self.name}')"

    def get_reference(self) -> dict:
        if self.default_value is not None:
            return {
                self.name: {"type": self.param_type, "defaultValue": self.default_value}
            }
        return {self.name: {"type": self.param_type}}
