import logging
import uuid

import cloecore.to_airflow.model.tasks as tasks
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def batchsteps_to_tasks(
    batchsteps: list[meta.Batchstep],
    jobs: dict[uuid.UUID, meta.DB2FS | meta.FS2DB | meta.ExecSQLJob],
    connections: dict[uuid.UUID, meta.Connection],
) -> list[
    tasks.SnowflakeFS2DBTask
    | tasks.SnowflakeExecutorTask
    | tasks.ODBCDB2FSTask
    | tasks.ODBCFS2DBTask
]:
    filecatalog_connections_id = [
        k for k, conn in connections.items() if conn.is_file_catalog_connection
    ][0]
    batchstep_tasks: list[
        tasks.SnowflakeFS2DBTask
        | tasks.SnowflakeExecutorTask
        | tasks.ODBCDB2FSTask
        | tasks.ODBCFS2DBTask
    ] = []
    for batchstep in batchsteps:
        job = jobs[batchstep.id]
        if isinstance(job, meta.ExecSQLJob):
            batchstep_tasks.append(
                execsql_to_task(batchstep.id, batchstep.get_dependencies(), job)
            )
        if isinstance(job, meta.DB2FS):
            batchstep_tasks.append(
                db2fs_to_task(
                    batchstep.id,
                    batchstep.get_dependencies(),
                    job,
                    filecatalog_connections_id,
                )
            )
        if isinstance(job, meta.FS2DB):
            batchstep_tasks.append(
                fs2db_to_task(
                    batchstep.id,
                    batchstep.get_dependencies(),
                    job,
                    filecatalog_connections_id,
                )
            )
    return batchstep_tasks


def execsql_to_task(
    task_id: uuid.UUID, task_dependencies: list[uuid.UUID], job: meta.ExecSQLJob
) -> tasks.SnowflakeExecutorTask:
    if job.sink_connection.is_snowflake_nativ:
        task = tasks.SnowflakeExecutorTask(
            name=job.name,
            task_n=task_id,
            depends_on=task_dependencies,
            sql_query=job.get_procedure_call_query(),
            connection_id=job.connection_id,
        )
    else:
        logger.error(
            "Connection type in Exec_SQL %s not implemented",
            job.sink_connection.system_type,
        )
        raise NotImplementedError
    logger.debug("Task for %s created", job.name)
    return task


def fs2db_to_task(
    task_id: uuid.UUID,
    task_dependencies: list[uuid.UUID],
    job: meta.FS2DB,
    filecatalog_connections_id: uuid.UUID,
) -> tasks.SnowflakeFS2DBTask | tasks.ODBCFS2DBTask:
    exec_query = None
    if job.postload_execjob is not None:
        exec_query = job.postload_execjob.get_procedure_call_query()
    sink_table_identifier = job.sink_connection.get_object_identifier(
        schema_name=job.sink_table.schema_name,
        object_name=job.sink_table.name,
    )
    task: tasks.SnowflakeFS2DBTask | tasks.ODBCFS2DBTask
    if job.sink_connection.is_snowflake_nativ:
        task = tasks.SnowflakeFS2DBTask(
            name=job.name,
            task_n=task_id,
            depends_on=task_dependencies,
            source_connections_id=job.source_connection_id,
            stage_name=job.source_connection.name,
            source_file_path_pattern=job.rendered_folder_path_pattern,
            source_file_name_pattern=job.rendered_filename_pattern,
            source_file_format=job.ds_type.storage_format,
            dataset_type_id=job.dataset_type_id,
            sink_connections_id=job.sink_connection_id,
            sink_table=sink_table_identifier,
            get_from_filecatalog=job.get_from_filecatalog,
            filecatalog_connections_id=filecatalog_connections_id,
            postload_job_call_query=exec_query,
        )
    elif (
        job.sink_connection.is_azure_sql_nativ
        or job.sink_connection.is_sql_server_nativ
    ):
        task = tasks.ODBCFS2DBTask(
            name=job.name,
            task_n=task_id,
            depends_on=task_dependencies,
            source_connections_id=job.source_connection_id,
            container_name=job.container_name,
            source_file_path_pattern=job.rendered_folder_path_pattern,
            source_file_name_pattern=job.rendered_filename_pattern,
            source_file_format=job.ds_type.name,
            dataset_type_id=job.dataset_type_id,
            sink_connections_id=job.sink_connection_id,
            sink_table=sink_table_identifier,
            get_from_filecatalog=job.get_from_filecatalog,
            filecatalog_connections_id=filecatalog_connections_id,
            postload_job_call_query=exec_query,
        )
    else:
        logger.error(
            "Connection type in FS2DB %s not implemented",
            job.sink_connection.system_type,
        )
        raise NotImplementedError
    logger.debug("Task for %s created", job.name)
    return task


def db2fs_to_task(
    task_id: uuid.UUID,
    task_dependencies: list[uuid.UUID],
    job: meta.DB2FS,
    filecatalog_connections_id: uuid.UUID,
) -> tasks.ODBCDB2FSTask:
    if (
        job.source_connection.azure_server_nativ_key
        or job.source_connection.sql_server_nativ_key
    ):
        task = tasks.ODBCDB2FSTask(
            name=job.name,
            task_n=task_id,
            depends_on=task_dependencies,
            source_connections_id=job.source_connection_id,
            select_statement=job.render_select_statement(),
            container_name=job.container_name,
            folder_path=job.rendered_folder_path,
            sink_file_name=job.get_sink_file_name(),
            sink_file_format="parquet",
            datasource_info_id=job.datasource_info_id,
            dataset_type_id=job.dataset_type_id,
            sink_connections_id=job.sink_connection_id,
            filecatalog_connections_id=filecatalog_connections_id,
        )
    else:
        logger.error(
            "Connection type in DB2FS %s not implemented",
            job.source_connection.system_type,
        )
        raise NotImplementedError
    logger.debug("Task for %s created", job.name)
    return task
