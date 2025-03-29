from cloecore.to_datafactory.arm.general.base import ARMBase


class Template:
    def __init__(self, resources: list[ARMBase]) -> None:
        self.resources = resources
        self.parameters: dict[str, dict] = {}
        self.variables: dict[str, str] = {}
        self.arm_schema = (
            "https://schema.management.azure.com/schemas/"
            "2019-04-01/deploymentTemplate.json#"
        )

    def get_parameters(self) -> None:
        for i in self.resources:
            self.parameters |= i.required_arm_parameters or {}

    def get_variables(self) -> None:
        for i in self.resources:
            self.variables |= i.required_arm_variables or {}

    def to_arm_template(self) -> dict[str, str | dict | list]:
        resources = [arm.to_arm() for arm in self.resources]
        self.get_parameters()
        self.get_variables()
        return {
            "$schema": self.arm_schema,
            "contentVersion": "1.0.0.0",
            "parameters": self.parameters,
            "variables": self.variables,
            "resources": resources,
        }

    def to_arm_parameter_file(self) -> dict[str, str | dict]:
        tem_parameters = {}
        for name, properties in self.parameters.items():
            if "defaultValue" in properties:
                tem_parameters[name] = {"value": properties["defaultValue"]}
            else:
                tem_parameters[name] = {"value": None}
        return {
            "$schema": self.arm_schema,
            "contentVersion": "1.0.0.0",
            "parameters": tem_parameters,
        }
