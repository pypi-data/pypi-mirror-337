import cloecore.to_datafactory.arm.general.parameter as param
from cloecore.to_datafactory.arm.general.base import ARMBase
from cloecore.utils.model import Connection


class LinkedServiceBase(ARMBase):
    """Base object for all linked services
    inherits from ARMBase.
    """

    type_short: str = "linkedService"
    type_fullpath: str = "Microsoft.DataFactory/factories/linkedservices"
    reference_type_name: str = "LinkedServiceReference"

    def __init__(
        self,
        name: str,
        connection: Connection,
        depends_on: list | None = None,
        required_arm_parameters: dict[str, dict] | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name, depends_on, required_arm_parameters, required_arm_variables
        )
        self.connection = connection
        self.depends_on += [
            (
                "[resourceId('Microsoft.DataFactory/factories',"
                f" {param.Parameter('factoryName').get_expression()})]"
            )
        ]
        self.required_arm_parameters |= param.Parameter("factoryName").get_reference()
