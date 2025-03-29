import uuid
from typing import Union

import cloecore.utils.model as meta
from cloecore.to_datafactory.arm.datafactory import (
    activities,
    custom_activities,
    datasets,
    linked_services,
    pipeline_resource,
)
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity
from cloecore.to_datafactory.packages import ExecSQLPackage
from cloecore.to_datafactory.packages.base import Package


def create_filecatalog_dataset(
    fc_ls: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService,
) -> datasets.AzureSqlDataset | datasets.AzureSynapseAnalyticsDataset:
    if isinstance(fc_ls, linked_services.AzureSqlLinkedService):
        return datasets.AzureSqlDataset(
            name="FileCatalog",
            linked_service=fc_ls,
            folder_name="Auxiliary",
        )
    return datasets.AzureSynapseAnalyticsDataset(
        name="FileCatalog",
        linked_service=fc_ls,
        folder_name="Auxiliary",
    )


def create_file_catalog_activity(
    job: meta.FS2DB,
    fc_ls: linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.AzureSqlLinkedService
    | linked_services.SnowflakeLinkedService,
) -> (
    tuple[
        custom_activities.MSSQLFileCatalogUpdateSuccessActivity,
        custom_activities.MSSQLFileCatalogUpdateFailureActivity,
    ]
    | tuple[
        custom_activities.SnowflakeFileCatalogUpdateSuccessActivity,
        custom_activities.SnowflakeFileCatalogUpdateFailureActivity,
    ]
    | tuple[
        custom_activities.SnowflakeFileCatalogPastInsertSuccessActivity,
        custom_activities.SnowflakeFileCatalogPastInsertFailureActivity,
    ]
):
    """This function takes in a job and an filecatalog ds resourse. Based
    on job settings and filecatalogs target it returns different
    filecatalog activites.

    Args:
        job (meta.FS2DB): _description_
        fc_ds (adf.DatasetResource): _description_

    Returns:
        tuple[custom_activities.MSSQLFileCatalogUpdateSuccessActivity]: _description_
    """
    if job.get_from_filecatalog and isinstance(
        fc_ls,
        (
            linked_services.AzureSynapseAnalyticsLinkedService,
            linked_services.AzureSqlLinkedService,
        ),
    ):
        return (
            custom_activities.MSSQLFileCatalogUpdateSuccessActivity(fc_ls),
            custom_activities.MSSQLFileCatalogUpdateFailureActivity(fc_ls),
        )
    if job.get_from_filecatalog and isinstance(
        fc_ls, linked_services.SnowflakeLinkedService
    ):
        return (
            custom_activities.SnowflakeFileCatalogUpdateSuccessActivity(
                linked_service=fc_ls
            ),
            custom_activities.SnowflakeFileCatalogUpdateFailureActivity(
                linked_service=fc_ls
            ),
        )
    if not job.get_from_filecatalog and isinstance(
        fc_ls, linked_services.SnowflakeLinkedService
    ):
        return (
            custom_activities.SnowflakeFileCatalogPastInsertSuccessActivity(fc_ls),
            custom_activities.SnowflakeFileCatalogPastInsertFailureActivity(fc_ls),
        )
    raise NotImplementedError


def create_get_activity(
    job: meta.FS2DB,
    fc_ds: datasets.AzureSqlDataset
    | datasets.AzureSynapseAnalyticsDataset
    | None = None,
    sink_ls: linked_services.SnowflakeLinkedService | None = None,
) -> Union[
    custom_activities.MSSQLFileCatalogGetActivity,
    custom_activities.SnowflakeRetrieveFilesFromBlobActivity,
    custom_activities.SnowflakeFileCatalogGetActivity,
]:
    """Helper function to decide if script activity or lookup activity needs to
    be used to retrieve files.

    Args:
        get_from_filecatalog (bool): _description_
        file_path_pattern (str): _description_
        file_name_pattern (str): _description_
        fc_ds (adf.DatasetResource): _description__

    Returns:
        Union[custom_activities.MSSQLFileCatalogGetActivity, custom_activities.
        SnowflakeRetrieveFilesFromBlobActivity]: _description_
    """
    if job.get_from_filecatalog and isinstance(
        fc_ds, (datasets.AzureSqlDataset, datasets.AzureSynapseAnalyticsDataset)
    ):
        return custom_activities.MSSQLFileCatalogGetActivity(
            file_path_pattern=job.rendered_folder_path_pattern,
            file_name_pattern=job.rendered_filename_pattern,
            source_ds=fc_ds,
        )
    if job.get_from_filecatalog and sink_ls is not None:
        return custom_activities.SnowflakeFileCatalogGetActivity(
            file_path_pattern=job.rendered_folder_path_pattern,
            file_name_pattern=job.rendered_filename_pattern,
            linked_service=sink_ls,
        )
    if not job.get_from_filecatalog and sink_ls is not None:
        return custom_activities.SnowflakeRetrieveFilesFromBlobActivity(
            file_path_pattern=job.rendered_folder_path_pattern,
            file_name_pattern=job.rendered_filename_pattern,
            linked_service=sink_ls,
        )
    raise NotImplementedError


def create_copy_activity(
    job: meta.FS2DB,
    linked_service: linked_services.SnowflakeLinkedService | None = None,
    source_ds: datasets.ParquetDataset | None = None,
    sink_ds: datasets.AzureSqlDataset
    | datasets.AzureSynapseAnalyticsDataset
    | None = None,
) -> custom_activities.CopyDataViaScriptActivity | custom_activities.FS2DBCopyActivity:
    """Function takes in a job and datasets. Generates a copy activity based
    on sink type.

    Args:
        job (meta.FS2DB): _description_
        source_ds (custom_activities.DatasetResource): _description_
        sink_ds (custom_activities.DatasetResource): _description_
        linked_service (linked_services.DatabaseLinkedService): _description_

    Raises:
        NotImplementedError: _description_

    Returns:
        Union[custom_activities.CopyDataViaScriptActivity, custom_activities.
        FS2DBCopyActivity]: _description_
    """
    sink_table_identifier = job.sink_connection.get_object_identifier(
        schema_name=job.sink_table.schema_name,
        object_name=job.sink_table.name,
    )
    if isinstance(linked_service, linked_services.SnowflakeLinkedService):
        return custom_activities.CopyDataViaScriptActivity(
            name="Copy to DB",
            description=job.description,
            source_ls_name=job.source_connection.name,
            table_identifier=sink_table_identifier,
            ds_type=job.ds_type,
            get_from_filecatalog=job.get_from_filecatalog,
            linked_service=linked_service,
        )
    if sink_ds is not None and source_ds is not None:
        return custom_activities.FS2DBCopyActivity(
            description=job.description,
            source_ds=source_ds,
            sink_ds=sink_ds,
            sink_schema_name=job.sink_table.schema_name,
            sink_table_name=job.sink_table.name,
            sink_table_identifier=sink_table_identifier,
        )
    raise NotImplementedError


def create_process_files_caller_activity(
    job: meta.FS2DB,
    load_pipeline: pipeline_resource.PipelineResource,
    foreach_activity: activities.ForEachActivity,
) -> activities.ExecutePipelineActivity:
    """Function takes in a a job and pipeline activity and a foreach activity. It
    creates a execute pipeline activity, which calls the pipeline with different
    parameters base on if files are retrieved from file catalog on snowflake or
    from a file catalog table.

    Args:
        job (meta.FS2DB): _description_
        load_pipeline (activities.PipelineResource): _description_
        foreach_activity (activities.ForEachActivity): _description_

    Raises:
        NotImplementedError: _description_

    Returns:
        activities.ExecutePipelineActivity: _description_
    """
    if job.sink_connection.is_snowflake_nativ:
        return custom_activities.SnowflakeProcessFilesExecutePipelineActivity(
            name=f"Execute_{job.get_short_id()}",
            pipeline=load_pipeline,
            foreach=foreach_activity,
            get_from_filecatalog=job.get_from_filecatalog,
        )
    if (
        job.get_from_filecatalog
        and job.sink_connection.is_azure_sql_nativ
        or job.sink_connection.is_synapse_nativ
    ):
        return custom_activities.MSSQLProcessFilesExecutePipelineActivity(
            name=f"Execute_{job.get_short_id()}",
            pipeline=load_pipeline,
            foreach=foreach_activity,
        )
    raise NotImplementedError


def create_datasets(
    dataset_base_name: str,
    fs_linked_service_container: str,
    fs_linked_service: linked_services.AzureBlobStorageLinkedService,
    db_linked_service: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService,
) -> tuple[
    datasets.ParquetDataset,
    datasets.AzureSqlDataset | datasets.AzureSynapseAnalyticsDataset,
]:
    ds_in_location = datasets.AzureBlobLocation(fs_linked_service_container)
    ds_out: datasets.AzureSqlDataset | datasets.AzureSynapseAnalyticsDataset
    ds_in = datasets.ParquetDataset(
        name=f"{dataset_base_name}_source",
        linked_service=fs_linked_service,
        location=ds_in_location,
        folder_name="FS2DB/source",
    )
    if isinstance(db_linked_service, linked_services.AzureSqlLinkedService):
        ds_out = datasets.AzureSqlDataset(
            name=f"{dataset_base_name}_sink",
            linked_service=db_linked_service,
            folder_name="FS2DB/sink",
        )
    elif isinstance(
        db_linked_service, linked_services.AzureSynapseAnalyticsLinkedService
    ):
        ds_out = datasets.AzureSynapseAnalyticsDataset(
            name=f"{dataset_base_name}_sink",
            linked_service=db_linked_service,
            folder_name="FS2DB/sink",
        )
    return ds_in, ds_out


class FS2DBPackage(Package):
    """Wrapper class to includes all necessary
    classes for a FS2DB package including connections
    and dependencies between them.
    """

    def __init__(
        self,
        job: meta.FS2DB,
        source_ls: linked_services.AzureBlobStorageLinkedService,
        sink_ls: linked_services.AzureSynapseAnalyticsLinkedService
        | linked_services.AzureSqlLinkedService
        | linked_services.SnowflakeLinkedService,
        fc_ls: linked_services.AzureSynapseAnalyticsLinkedService
        | linked_services.AzureSqlLinkedService
        | linked_services.SnowflakeLinkedService,
        exec_job: ExecSQLPackage | None = None,
    ) -> None:
        super().__init__(job_id=job.id, job_name=job.name)
        self.postload_execjob = None
        if isinstance(
            fc_ls,
            (
                linked_services.AzureSynapseAnalyticsLinkedService,
                linked_services.AzureSqlLinkedService,
            ),
        ):
            fc_ds = create_filecatalog_dataset(fc_ls)
            self.start_activity = self.file_get_activity = create_get_activity(
                job=job, fc_ds=fc_ds
            )
            self.used_datasets.append(fc_ds)
        else:
            self.start_activity = self.file_get_activity = create_get_activity(
                job=job, sink_ls=fc_ls
            )
        if isinstance(
            sink_ls,
            (
                linked_services.AzureSynapseAnalyticsLinkedService,
                linked_services.AzureSqlLinkedService,
            ),
        ):
            source_ds, sink_ds = create_datasets(
                job.name, job.container_name, source_ls, sink_ls
            )
            self.used_datasets += [source_ds, sink_ds]
            self.copy_activity = create_copy_activity(
                job=job, source_ds=source_ds, sink_ds=sink_ds
            )
        else:
            self.copy_activity = create_copy_activity(job, sink_ls)
        fc_act_on_success, fc_act_on_failure = create_file_catalog_activity(job, fc_ls)
        self.fc_act_on_success: BaseActivity = fc_act_on_success
        self.fc_act_on_failure: BaseActivity = fc_act_on_failure
        aux_pipe_act: list[BaseActivity] = [
            self.copy_activity,
            self.fc_act_on_failure,
            self.fc_act_on_success,
        ]
        self.foreach_activity = custom_activities.FS2DBForeach(
            "Process files", self.file_get_activity
        )
        self.all_activities = [
            self.copy_activity,
            self.file_get_activity,
            self.fc_act_on_success,
            self.fc_act_on_failure,
            self.foreach_activity,
        ]
        if exec_job is not None:
            self.postload_execjob = exec_job.pipeline_activities[0]
            self.postload_execjob.name = "Run merge"
            aux_pipe_act.append(self.postload_execjob)
            self.all_activities.append(self.postload_execjob)
        load_pipeline = pipeline_resource.PipelineResource(
            name=f"Foreach_elements_{job.get_short_id()}", pipe_activities=aux_pipe_act
        )
        foreach_exec_pipe_activity = create_process_files_caller_activity(
            job, load_pipeline, self.foreach_activity
        )
        self.foreach_activity.add_activities([foreach_exec_pipe_activity])
        self.all_activities.append(foreach_exec_pipe_activity)
        self.end_activity = self.foreach_activity
        self.pipeline_activities = [self.file_get_activity, self.foreach_activity]
        self.pipeline = load_pipeline
        self._set_dependencies()

    def _set_dependencies(self) -> None:
        if self.postload_execjob is not None:
            self.postload_execjob.add_activity_dependency(
                self.copy_activity, "Succeeded"
            )
            self.fc_act_on_success.add_activity_dependency(
                self.postload_execjob, "Succeeded"
            )
            self.fc_act_on_failure.add_activity_dependency(
                self.postload_execjob, "Failed"
            )
        else:
            self.fc_act_on_success.add_activity_dependency(
                self.copy_activity, "Succeeded"
            )
            self.fc_act_on_failure.add_activity_dependency(self.copy_activity, "Failed")
        self.foreach_activity.add_activity_dependency(
            self.file_get_activity, "Succeeded"
        )

    def get_pipeline_counter(self) -> int:
        return len(self.pipeline_activities) + len(self.foreach_activity.activities)

    def _prepare_pipelines(self) -> None:
        self.pipeline.folder_name = f"{self.batch_name}/Auxiliary_Pipelines"

    def init_for_pipeline(self, batch_name: str, batchstep_id: uuid.UUID) -> None:
        super().init_for_pipeline(batch_name, batchstep_id)
        self._prepare_pipelines()
