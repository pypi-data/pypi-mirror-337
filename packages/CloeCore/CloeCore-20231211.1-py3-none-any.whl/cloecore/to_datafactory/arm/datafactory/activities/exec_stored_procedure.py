import logging

from cloecore.to_datafactory.arm.datafactory import linked_services
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity

logger = logging.getLogger(__name__)


class ExecuteStoredProcedureActivity(BaseActivity):
    """Base line activity for ExecuteStoredProcedure. Wraps
    BaseActivity.
    """

    def __init__(
        self,
        name: str,
        linked_service: linked_services.AzureSqlLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService,
        stored_procedure_identifier: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            act_depends_on=act_depends_on,
            res_depends_on=linked_service.get_dependency_on(),
        )
        self.stored_procedure_identifier = stored_procedure_identifier
        self.stored_procedure_params: dict[str, dict] = {}
        self.linked_service_ref = linked_service.get_reference()

    def _get_arm_stored_procedure_identifier(self) -> str:
        if self.stored_procedure_identifier[0] == "[":
            return f"[{self.stored_procedure_identifier}"
        return self.stored_procedure_identifier

    def _create_parameter(
        self, name: str, param_type: str, value: str | dict[str, str] | bool
    ) -> None:
        self.stored_procedure_params[name] = {"type": param_type, "value": value}

    def _to_arm(self) -> dict:
        return {
            "type": "SqlServerStoredProcedure",
            "policy": {
                "timeout": "0.08:00:00",
                "retry": 0,
                "retryIntervalInSeconds": 30,
                "secureOutput": False,
                "secureInput": False,
            },
            "typeProperties": {
                "storedProcedureName": self._get_arm_stored_procedure_identifier(),
                "storedProcedureParameters": self.stored_procedure_params,
            },
            "linkedServiceName": self.linked_service_ref,
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        base = super().to_arm()
        base |= self._to_arm()
        return base
