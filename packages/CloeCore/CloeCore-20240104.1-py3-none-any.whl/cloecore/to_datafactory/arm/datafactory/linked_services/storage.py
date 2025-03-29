import cloecore.to_datafactory.arm.general.parameter as param
from cloecore.to_datafactory.arm.datafactory.linked_services.base import (
    LinkedServiceBase,
)
from cloecore.utils.model.jobs.connections import Connection


class AzureBlobStorageLinkedService(LinkedServiceBase):
    """Wrapper class for LinkedServiceBase. Intermediate class
    for creating LinkedServices for azure blob systems.
    """

    property_type = "AzureBlobStorage"

    def __init__(
        self,
        name: str,
        connection: Connection,
        secret_reference: dict,
        depends_on: list | None = None,
        required_arm_parameters: dict[str, dict] | None = None,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name,
            connection,
            depends_on,
            required_arm_parameters,
            required_arm_variables,
        )
        self.account_key = secret_reference
        self.annotations: list[str] = []
        self.required_arm_parameters |= param.Parameter(
            f"ConnectVia{self.name}", default_value="null"
        ).get_reference()

    def _to_arm(self) -> dict:
        connect_via = (
            f"[if(equals(parameters('ConnectVia{self.name}'), 'null'),"
            f" null(), createObject('referenceName', parameters('ConnectVia{self.name}'"
            "), 'type', 'IntegrationRuntimeReference'))]"
        )
        return {
            "type": self.property_type,
            "typeProperties": {"connectionString": self.account_key},
            "connectVia": connect_via,
            "annotations": self.annotations,
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        self.properties = self._to_arm()
        return super().to_arm()
