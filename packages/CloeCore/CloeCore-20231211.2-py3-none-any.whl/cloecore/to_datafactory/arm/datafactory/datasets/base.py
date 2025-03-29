import cloecore.to_datafactory.arm.general.parameter as param
from cloecore.to_datafactory.arm.datafactory.linked_services import base
from cloecore.to_datafactory.arm.general.base import ARMBase


class DatasetResource(ARMBase):
    type_short: str = "datasets"
    type_fullpath: str = "Microsoft.DataFactory/factories/datasets"
    reference_type_name: str = "DatasetReference"

    def __init__(
        self,
        name: str,
        linked_service: base.LinkedServiceBase,
        folder_name: str,
        annotations: list[str] | None = None,
        schema: list | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        deps = linked_service.get_dependency_on()
        deps.append(
            (
                "[resourceId('Microsoft.DataFactory/factories',"
                f" {param.Parameter('factoryName').get_expression()})]"
            )
        )
        super().__init__(
            name=name,
            depends_on=deps,
            required_arm_parameters=param.Parameter("factoryName").get_reference(),
            required_arm_variables=required_arm_variables,
        )
        self.linked_service = linked_service
        self.linked_service_ref = linked_service.get_reference()
        self.folder_name = folder_name
        self.input_parameters: dict[str, dict] = {}
        self.schema = schema or []
        self.annotations = annotations or []

    def _create_parameter(self, name: str) -> None:
        self.input_parameters[name] = {"type": "string"}

    def _get_parameter_expression(self, name: str) -> dict:
        return {"value": f"@dataset().{name}", "type": "Expression"}

    def get_inputs(self) -> list[str]:
        return list(self.input_parameters.keys())

    def to_arm(self) -> dict[str, dict | str | list]:
        self.properties["folder"] = {"name": self.folder_name}
        self.properties["linkedServiceName"] = self.linked_service_ref
        self.properties["parameters"] = self.input_parameters
        self.properties["schema"] = self.schema
        self.properties["annotations"] = self.schema
        return super().to_arm()
