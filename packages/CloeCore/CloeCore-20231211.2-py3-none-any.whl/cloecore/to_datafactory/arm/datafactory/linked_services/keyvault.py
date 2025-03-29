import cloecore.to_datafactory.arm.datafactory.variables as var
import cloecore.to_datafactory.arm.general.parameter as param
from cloecore.to_datafactory.arm.general.base import ARMBase


class AzureKeyVaultLinkedService(ARMBase):
    """Resembles the AzureKeyVault linked service in
    ADF. Inherits from LinkedServiceBase class.
    """

    type_short: str = "linkedService"
    type_fullpath: str = "Microsoft.DataFactory/factories/linkedservices"
    reference_type_name: str = "LinkedServiceReference"

    property_type: str = "AzureKeyVault"

    def __init__(
        self,
        depends_on: list | None = None,
        required_arm_parameters: dict[str, dict] | None = None,
    ) -> None:
        vault_url = "[concat('https://', parameters('vaultName'), '.vault.azure.net')]"
        super().__init__(
            name=param.Parameter("vaultName"),
            depends_on=depends_on,
            required_arm_parameters=required_arm_parameters,
            required_arm_variables={"vaultName": vault_url},
        )
        self.depends_on += [
            (
                "[resourceId('Microsoft.DataFactory/factories',"
                f" {param.Parameter('factoryName').get_expression()})]"
            )
        ]
        self.required_arm_parameters |= param.Parameter("factoryName").get_reference()
        self.base_url = var.Variable("vaultName").get_standalone()

    def get_secret_reference(self, name: str):
        """Returns a secret reference that can be used in
        an ADF resources. At query the ADF will requests the
        secrets value.

        Args:
            name (str): _description_

        Returns:
            _type_: _description_
        """
        return {
            "type": "AzureKeyVaultSecret",
            "store": self.get_reference(),
            "secretName": name,
        }

    def _to_arm(self) -> dict:
        return {
            "type": self.property_type,
            "typeProperties": {"baseUrl": self.base_url},
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        self.properties = self._to_arm()
        return super().to_arm()
