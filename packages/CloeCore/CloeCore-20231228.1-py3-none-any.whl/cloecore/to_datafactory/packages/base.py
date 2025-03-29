from __future__ import annotations

import uuid

import cloecore.to_datafactory.packages as packages
import cloecore.utils.model as meta
from cloecore.to_datafactory.arm.datafactory import datasets
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity


class Package:
    def __init__(
        self,
        job_id: uuid.UUID,
        job_name: str,
        start_activity: BaseActivity | None = None,
        end_activity: BaseActivity | None = None,
    ) -> None:
        self.start_activity = start_activity
        self.end_activity = end_activity
        self.all_activities: list[BaseActivity] = []
        self.pipeline_activities: list[BaseActivity] = []
        self.job_id = job_id
        self.job_name = job_name
        self.used_datasets: list[
            datasets.AzureSqlDataset
            | datasets.AzureSynapseAnalyticsDataset
            | datasets.SqlServerDataset
            | datasets.SnowflakeDataset
            | datasets.OracleDataset
            | datasets.DB2Dataset
            | datasets.ParquetDataset
            | datasets.PostgreSQLDataset
            | datasets.AzurePostgreSQLDataset
        ] = []

    def set_start_dependency(
        self,
        batchstep: meta.Batchstep,
        batchstep_id_to_package: dict[
            uuid.UUID,
            packages.ExecSQLPackage | packages.DB2FSPackage | packages.FS2DBPackage,
        ],
    ) -> None:
        # reset dependencies for first activity to avoid clash with previous runs
        if self.start_activity is not None and batchstep.dependencies is not None:
            self.start_activity.act_depends_on = []
            for i in batchstep.dependencies:
                if (
                    job := batchstep_id_to_package[
                        i.dependent_on_batchstep_id
                    ].end_activity
                ) is not None:
                    if i.ignore_dependency_failed_state:
                        self.start_activity.add_activity_dependency(job, "Completed")
                    else:
                        self.start_activity.add_activity_dependency(job, "Succeeded")

    def get_pipeline_counter(self) -> int:
        return len(self.pipeline_activities)

    def _set_activity_user_properties(self) -> None:
        for act in self.all_activities:
            act.set_user_properties(
                job_id=self.job_id,
                job_name=self.job_name,
                batchstep_id=self.batchstep_id,
            )

    def init_for_pipeline(self, batch_name: str, batchstep_id: uuid.UUID) -> None:
        self.batch_name = batch_name
        self.batchstep_id = batchstep_id
        self._set_activity_user_properties()

    def adjust_name_of_activites(self, postfix: int) -> None:
        for activity in self.pipeline_activities:
            activity.name = f"{activity.name[:(55-len(str(postfix)))]} {postfix}"
