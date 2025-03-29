import logging

from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity
from cloecore.to_datafactory.arm.datafactory.linked_services import database

logger = logging.getLogger(__name__)


class ScriptActivity(BaseActivity):
    """ADF script activity. Should not be used
    directly.
    """

    def __init__(
        self,
        name: str,
        linked_service: database.DatabaseLinkedService,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name,
            description,
            act_depends_on,
            res_depends_on=linked_service.get_dependency_on(),
        )
        self.query_params: dict[str, dict[str, str | dict[str, str]]] = {}
        self.scripts: list[dict[str, dict | str | list]] = []
        self.linked_service_ref = linked_service.get_reference()
        self.linked_service_type = linked_service.property_type

    def _create_parameter(
        self, name: str, param_type: str, value: str | dict[str, str]
    ) -> None:
        """Creates a Script parameter which can be used by the ADF
        to input values in a save way into the query.

        Args:
            name (str): _description_
            param_type (str): _description_
            value (str): _description_
        """
        self.query_params[name] = {
            "name": name,
            "type": param_type,
            "value": value,
            "direction": "Input",
        }

    def _to_arm(self) -> dict:
        return {
            "type": "Script",
            "policy": {
                "timeout": "0.08:00:00",
                "retry": 0,
                "retryIntervalInSeconds": 30,
                "secureOutput": False,
                "secureInput": False,
            },
            "linkedServiceName": self.linked_service_ref,
            "typeProperties": {
                "scripts": self.scripts,
                "logSettings": {"logDestination": "ActivityOutput"},
            },
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        """Transforms the class to an ARM template
        snippet.

        Returns:
            dict: _description_
        """
        base = super().to_arm()
        base |= self._to_arm()
        return base
