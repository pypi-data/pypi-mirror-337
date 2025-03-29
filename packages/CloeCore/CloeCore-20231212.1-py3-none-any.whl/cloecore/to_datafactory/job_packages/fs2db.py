import cloecore.utils.model as meta
from cloecore.to_datafactory import factory_objects
from cloecore.utils import model


def transform_fs2db_to_factory_object(
    job: model.FS2DB, batchstep: meta.Batchstep
) -> factory_objects.ExecutePipelineActivity:
    """This function can be used to generate the ExecutePipeline activity to call the job pipeline
    in the template adf. It will use the metadata from the fs2db job to generate the parameter values.

    Args:
        job (model.FS2DB): _description_

    Returns:
        factory_objects.ExecutePipelineActivity: _description_
    """
    parameters = {
        "filePathPattern": job.rendered_folder_path_pattern,
        "fileNamePattern": job.rendered_filename_pattern,
        "datasetName": job.ds_type.name,
        "tableFQDN": job.sink_table.get_table_identifier(),
        "stageName": job.source_connection.name,
    }
    type_properties = factory_objects.ExecutePipelineTypeProperties(
        parameters=parameters,
        pipeline={
            "referenceName": f"job_fs2db_{job.source_connection.name}_{job.sink_connection.name}",
            "type": "PipelineReference",
        },
    )
    execute_pipeline = factory_objects.ExecutePipelineActivity(
        name=batchstep.name, type_properties=type_properties, batchstep_id=batchstep.id
    )
    return execute_pipeline
