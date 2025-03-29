import logging

import cloecore.to_datafactory.arm.general.parameter as param

logger = logging.getLogger(__name__)


class ARMBase:
    api_version = "2018-06-01"
    type_short: str = "base"
    type_fullpath: str = "Microsoft.DataFactory/factories/base"
    reference_type_name: str = "BaseReference"

    def __init__(
        self,
        name: str | param.Parameter,
        depends_on: list | None = None,
        required_arm_parameters: dict[str, dict] | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        self.name = name
        self.depends_on = depends_on or []
        self.required_arm_parameters = required_arm_parameters or {}
        self.required_arm_variables = required_arm_variables or {}
        if isinstance(self.name, param.Parameter):
            self.required_arm_parameters |= self.name.get_reference()
        self.properties: dict[str, dict | str | list] = {}

    @property
    def name(self) -> str | param.Parameter:
        return self._name

    @name.setter
    def name(self, name: str | param.Parameter) -> None:
        if isinstance(name, str):
            if len(name) > 140:
                logger.warning(
                    (
                        "Length of %s name %s is %s but must not exceed 140."
                        "It was shortened."
                    ),
                    self.type_short,
                    name,
                    len(name),
                )
                name = name[0:140]
        self._name = name

    def _get_arm_name(self) -> str:
        if isinstance(self.name, param.Parameter):
            return (
                "[concat(parameters('factoryName'), '/',"
                f" {self.name.get_expression()})]"
            )
        else:
            return f"[concat(parameters('factoryName'), '/{self.name}')]"

    def get_reference(
        self, parameters: dict | None = None
    ) -> dict[str, str | dict | param.Parameter]:
        ref_name = self.name
        if isinstance(self.name, param.Parameter):
            ref_name = self.name.get_standalone()
        if parameters:
            return {
                "referenceName": ref_name,
                "type": self.reference_type_name,
                "parameters": parameters,
            }
        return {"referenceName": ref_name, "type": self.reference_type_name}

    def get_dependency_on(self) -> list[str]:
        if isinstance(self.name, param.Parameter):
            return [
                (
                    f"[resourceId('{self.type_fullpath}', parameters('factoryName'),"
                    f" {self.name.get_expression()})]"
                )
            ]
        else:
            return [
                (
                    f"[resourceId('{self.type_fullpath}', parameters('factoryName'),"
                    f" '{self.name}')]"
                )
            ]

    def to_arm(self) -> dict[str, dict | str | list]:
        return {
            "name": self._get_arm_name(),
            "type": self.type_fullpath,
            "apiVersion": self.api_version,
            "properties": self.properties,
            "dependsOn": list(set(self.depends_on)),
        }
