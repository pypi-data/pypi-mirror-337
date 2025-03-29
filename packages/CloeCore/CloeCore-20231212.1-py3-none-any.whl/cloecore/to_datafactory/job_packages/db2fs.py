import cloecore.utils.model as meta
from cloecore.to_datafactory import factory_objects
from cloecore.utils import model


def transform_db2fs_to_factory_object(
    job: model.DB2FS, batchstep: meta.Batchstep
) -> factory_objects.ExecutePipelineActivity:
    """This function can be used to generate the ExecutePipeline activity to call the job pipeline
    in the template adf. It will use the metadata from the db2fs job to generate the parameter values.

    Args:
        job (model.DB2FS): _description_

    Returns:
        factory_objects.ExecutePipelineActivity: _description_
    """
    parameters = {
        "fileNameContent": job.ds_info.content,
        "fileNameSourcesystemName": job.ds_info.sourcesystem.name,
        "fileNameTenantName": job.ds_info.tenant.name
        if job.ds_info.tenant is not None
        else None,
        "fileNameObjectDescription": job.ds_info.object_description,
        "fileNameDatasetTypeName": job.ds_type.name,
        "sourceSchemaName": job.source_table.rendered_schema_name,
        "sourceTableName": job.source_table.rendered_name,
        "sourceSelectQuery": job.render_select_statement(),
        "fileFolderPath": job.rendered_folder_path,
        "dataSourceInfoID": str(job.datasource_info_id),
        "sourceConnectionID": str(job.source_connection_id),
        "sinkConnectionID": str(job.sink_connection_id),
        "datasetTypeID": str(job.dataset_type_id),
    }
    type_properties = factory_objects.ExecutePipelineTypeProperties(
        parameters=parameters,
        pipeline={
            "referenceName": f"job_db2fs_{job.source_connection.name}_{job.sink_connection.name}",
            "type": "PipelineReference",
        },
    )
    execute_pipeline = factory_objects.ExecutePipelineActivity(
        name=batchstep.name, type_properties=type_properties, batchstep_id=batchstep.id
    )
    return execute_pipeline
