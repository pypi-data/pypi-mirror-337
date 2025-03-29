from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity


class SetVariableActivity(BaseActivity):
    """Set variable activity wraps BaseActivity."""

    def __init__(
        self,
        name: str,
        variable_value: str | dict,
        variable_name: str | None = None,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(name, description, act_depends_on, res_depends_on)
        self._variable_name = variable_name
        self.variable_value = variable_value

    @property
    def variable_name(self) -> str:
        return self._variable_name or f"{self.name.lower().replace(' ', '_')}.store"

    def _to_arm(self) -> dict:
        return {
            "type": "SetVariable",
            "typeProperties": {
                "variableName": self.variable_name,
                "value": self.variable_value,
            },
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        self.pipeline_variables.append(self.variable_name)
        base = super().to_arm()
        base |= self._to_arm()
        return base
