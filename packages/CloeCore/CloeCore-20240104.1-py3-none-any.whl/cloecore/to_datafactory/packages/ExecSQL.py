import logging

import cloecore.utils.model as meta
from cloecore.to_datafactory.arm.datafactory import (
    activities,
    custom_activities,
    linked_services,
)
from cloecore.to_datafactory.packages.base import Package

logger = logging.getLogger(__name__)


class ExecSQLPackage(Package):
    def __init__(
        self,
        job: meta.ExecSQL,
        linked_service: linked_services.AzureSqlLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.SnowflakeLinkedService,
        stored_procedure_identifier: str,
        description: str | None = None,
    ) -> None:
        super().__init__(job.id, job.name)
        if isinstance(
            linked_service,
            (
                linked_services.AzureSqlLinkedService,
                linked_services.AzureSynapseAnalyticsLinkedService,
                linked_services.SqlServerLinkedService,
            ),
        ):
            self.start_activity = activities.ExecuteStoredProcedureActivity(
                name="Execute SQL Script",
                description=description,
                linked_service=linked_service,
                stored_procedure_identifier=stored_procedure_identifier,
            )
        elif isinstance(linked_service, linked_services.SnowflakeLinkedService):
            self.start_activity = (
                custom_activities.ExecuteStoredProcedureViaScriptActivity(
                    name="Execute SQL Script",
                    description=description,
                    linked_service=linked_service,
                    stored_procedure_identifier=stored_procedure_identifier,
                )
            )
        self.end_activity = self.start_activity
        self.all_activities = [self.start_activity]
        self.pipeline_activities = [self.start_activity]
