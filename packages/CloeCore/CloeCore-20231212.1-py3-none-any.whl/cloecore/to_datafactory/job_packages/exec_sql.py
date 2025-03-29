import cloecore.utils.model as meta
from cloecore.to_datafactory import factory_objects
from cloecore.utils import model


def transform_exec_sql_to_factory_object(
    job: model.ExecSQLJob, batchstep: meta.Batchstep
) -> factory_objects.ExecutePipelineActivity:
    """This function can be used to generate the ExecutePipeline activity to call the job pipeline
    in the template adf. It will use the metadata from the exec_sql job to generate the parameter values.

    Args:
        job (model.ExecSQLJob): _description_

    Returns:
        factory_objects.ExecutePipelineActivity: _description_
    """
    parameters = {
        "sqlQuery": job.get_procedure_call_query(),
    }
    type_properties = factory_objects.ExecutePipelineTypeProperties(
        parameters=parameters,
        pipeline={
            "referenceName": f"job_exec_sql_{job.sink_connection.name}",
            "type": "PipelineReference",
        },
    )
    execute_pipeline = factory_objects.ExecutePipelineActivity(
        name=batchstep.name, type_properties=type_properties, batchstep_id=batchstep.id
    )
    return execute_pipeline
