import cloecore.to_datafactory.arm.general.parameter as param
from cloecore.to_datafactory.arm.general import parameter
from cloecore.to_datafactory.arm.general.base import ARMBase


class Factory(ARMBase):
    type_short: str = "factories"
    type_fullpath: str = "Microsoft.DataFactory/factories"

    def __init__(
        self,
        depends_on: list | None = None,
        required_arm_parameters: dict[str, dict] | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name=parameter.Parameter("factoryName"),
            depends_on=depends_on,
            required_arm_parameters=required_arm_parameters,
            required_arm_variables=required_arm_variables,
        )
        self.location = parameter.Parameter(
            "location", default_value="[resourceGroup().location]"
        )
        self.identity = parameter.Parameter(
            "factoryIdentity", default_value="SystemAssigned"
        )
        self.tags = parameter.Parameter(
            "kvtags", param_type="object", default_value={"Managed-by": "CLOE"}
        )
        self.required_arm_parameters |= self.location.get_reference()
        self.required_arm_parameters |= self.identity.get_reference()
        self.required_arm_parameters |= self.tags.get_reference()
        self._factory_properties_param = param.Parameter(
            "FactoryProperties", param_type="object", default_value={}
        )
        self.required_arm_parameters |= self._factory_properties_param.get_reference()

    def _get_arm_name(self) -> str:
        if isinstance(self.name, parameter.Parameter):
            return self.name.get_standalone()
        else:
            return self.name

    def to_arm(self) -> dict[str, dict | str | list]:
        return dict(
            name=self._get_arm_name(),
            type=self.type_fullpath,
            apiVersion=self.api_version,
            tags=self.tags.get_standalone(),
            properties=self._factory_properties_param.get_standalone(),
            dependsOn=self.depends_on,
            location=self.location.get_standalone(),
            identity={"type": self.identity.get_standalone()},
        )
