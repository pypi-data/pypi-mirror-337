import logging
import uuid
from typing import cast

import cloecore.to_datafactory.packages as packages
import cloecore.to_datafactory.Utils as utils
import cloecore.utils.model as meta
from cloecore.to_datafactory.arm.datafactory import activities, linked_services, trigger
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity
from cloecore.to_datafactory.arm.datafactory.datasets import base
from cloecore.to_datafactory.arm.datafactory.linked_services.base import (
    LinkedServiceBase,
)
from cloecore.to_datafactory.arm.datafactory.pipeline_resource import PipelineResource
from cloecore.to_datafactory.factory.Activities import job_to_activity_package

logger = logging.getLogger(__name__)


def deduplicate_packages(
    activity_packages: dict[
        uuid.UUID,
        packages.ExecSQLPackage | packages.DB2FSPackage | packages.FS2DBPackage,
    ],
) -> None:
    activity_job_ids: dict[uuid.UUID, int] = {}
    for activity_package in activity_packages.values():
        if activity_package.job_id in activity_job_ids:
            activity_package.adjust_name_of_activites(
                activity_job_ids[activity_package.job_id]
            )
            activity_job_ids[activity_package.job_id] += 1
        else:
            activity_job_ids[activity_package.job_id] = 1


def prepare_batches_and_jobs(
    batch: meta.Batch,
    jobs: dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQL],
    id_to_ls: dict[uuid.UUID, LinkedServiceBase],
    fc_ls: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.SnowflakeLinkedService
    | None,
) -> tuple[
    str,
    dict[int, str],
    dict[int, list[uuid.UUID]],
    dict[
        uuid.UUID,
        packages.ExecSQLPackage | packages.DB2FSPackage | packages.FS2DBPackage,
    ],
]:
    activity_packages: dict[
        uuid.UUID,
        packages.ExecSQLPackage | packages.DB2FSPackage | packages.FS2DBPackage,
    ] = {}
    folder_root = f"{batch.name}"
    batchstep_to_job_id = {i.id: i.job_id for i in batch.batchsteps}
    for batchstep in batch.batchsteps:
        activity_packages[batchstep.id] = job_to_activity_package(
            jobs[batchstep_to_job_id[batchstep.id]], id_to_ls, fc_ls
        )
    deduplicate_packages(activity_packages)
    pipeline_build_plan = utils.optimize_batch(batch.batchsteps, activity_packages)
    pipeline_names = {i: f"{batch.name}_{i}" for i in pipeline_build_plan.keys()}
    return folder_root, pipeline_names, pipeline_build_plan, activity_packages


def create_pipeline_activities(
    batch: meta.Batch,
    pipeline: list[uuid.UUID],
    activity_packages: dict[
        uuid.UUID,
        packages.ExecSQLPackage | packages.DB2FSPackage | packages.FS2DBPackage,
    ],
) -> tuple[list[PipelineResource], list[BaseActivity]]:
    pipelines: list[PipelineResource] = []
    pipe_activities: list[BaseActivity] = []
    for batchstep_id in pipeline:
        activity_package = activity_packages[batchstep_id]
        activity_package.init_for_pipeline(batch.name, batchstep_id)
        if isinstance(activity_package, packages.FS2DBPackage):
            pipelines += [pipeline for pipeline in [activity_package.pipeline]]
        activity_package.set_start_dependency(
            batch.get_batchstep_by_id(batchstep_id), activity_packages
        )
        pipe_activities += activity_package.pipeline_activities
        logger.debug("Pipeline step %s created", batchstep_id)
    return pipelines, pipe_activities


def deduplicating_datasets(
    datasets: list[base.DatasetResource],
) -> list[base.DatasetResource]:
    existing_names = []
    dedup_datasets = []
    for dataset in datasets:
        if dataset.name not in existing_names:
            existing_names.append(dataset.name)
            dedup_datasets.append(dataset)
    return dedup_datasets


def create_master_pipeline(
    master_name: str, pipelines: list[PipelineResource], folder_name: str
) -> PipelineResource:
    pipe_activities: list[BaseActivity] = []
    for pipeline in pipelines:
        exec_pipe = activities.ExecutePipelineActivity(
            name=f"Execute {pipeline.name}", pipeline=pipeline
        )
        pipe_activities.append(exec_pipe)
    return PipelineResource(
        name=master_name, pipe_activities=pipe_activities, folder_name=folder_name
    )


def create_pipelines(
    batches: list[meta.Batch],
    jobs: dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQL],
    fc_ls: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.SnowflakeLinkedService
    | None,
    id_to_ls: dict[
        uuid.UUID,
        linked_services.AzureBlobStorageLinkedService
        | linked_services.AzureSqlLinkedService
        | linked_services.AzureSynapseAnalyticsLinkedService
        | linked_services.OracleLinkedService
        | linked_services.SnowflakeLinkedService
        | linked_services.SqlServerLinkedService
        | linked_services.DB2LinkedService
        | linked_services.PostgreSQLLinkedService
        | linked_services.AzurePostgreSQLLinkedService,
    ],
) -> tuple[list[base.DatasetResource], list[PipelineResource], list[trigger.Trigger]]:
    batch_adf_components: list[PipelineResource] = []
    used_datasets: list[base.DatasetResource] = []
    used_trigger: list[trigger.Trigger] = []
    id_to_ls_c = cast(dict[uuid.UUID, LinkedServiceBase], id_to_ls)
    for batch in batches:
        pipelines: dict[str, PipelineResource] = {}
        (
            folder_root,
            pipeline_names,
            pipeline_build_plan,
            activity_packages,
        ) = prepare_batches_and_jobs(batch, jobs, id_to_ls_c, fc_ls)
        for act in activity_packages.values():
            used_datasets += act.used_datasets
        for pipeline_id, pipeline in pipeline_build_plan.items():
            side_pipelines, pipe_activities = create_pipeline_activities(
                batch, pipeline, activity_packages
            )
            batch_adf_components.extend(side_pipelines)
            full_pipeline = PipelineResource(
                name=pipeline_names[pipeline_id],
                pipe_activities=pipe_activities,
                folder_name=f"{folder_root}/Pipelines",
            )
            pipelines[str(pipeline_id)] = full_pipeline
            logger.info("Pipeline %s created", pipeline_id)
        if len(pipeline_build_plan) > 1:
            pipeline_master_name = f"{batch.name}_master"
            pipelines["master"] = create_master_pipeline(
                pipeline_master_name, list(pipelines.values()), folder_root
            )
            logger.info("Pipeline master created")
            used_trigger.append(
                trigger.Trigger(
                    pipeline=pipelines["master"],
                    cron=batch.cron,
                    timezone=batch.timezone,
                )
            )
            logger.info("Pipeline trigger created")
        else:
            used_trigger.append(
                trigger.Trigger(
                    pipeline=list(pipelines.values())[0],
                    cron=batch.cron,
                    timezone=batch.timezone,
                )
            )
            logger.info("Pipeline trigger created")
        batch_adf_components += [i for i in pipelines.values()]
    return deduplicating_datasets(used_datasets), batch_adf_components, used_trigger
