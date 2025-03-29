import logging
import uuid

import cloecore.utils.model as meta
from cloecore.to_datafactory import packages
from cloecore.to_datafactory.arm.datafactory import linked_services
from cloecore.to_datafactory.arm.datafactory.linked_services.base import (
    LinkedServiceBase,
)

logger = logging.getLogger(__name__)


def job_to_activity_package(
    job: meta.FS2DB | meta.DB2FS | meta.ExecSQLJob,
    id_to_ls: dict[
        uuid.UUID,
        LinkedServiceBase,
    ],
    fc_ls: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.SnowflakeLinkedService
    | None,
) -> packages.ExecSQLPackage | packages.DB2FSPackage | packages.FS2DBPackage:
    if isinstance(job, meta.ExecSQLJob):
        return execsql_to_activities(job, id_to_ls)
    if isinstance(job, meta.FS2DB):
        exec_activity = None
        if job.postload_execjob is not None:
            exec_activity = execsql_to_activities(job.postload_execjob, id_to_ls)
        if fc_ls is None:
            raise ValueError("FS2DB jobs are used but no filecatalog connection set.")
        return fs2db_to_activities(job, id_to_ls, fc_ls, exec_activity)
    if isinstance(job, meta.DB2FS):
        if fc_ls is None:
            raise ValueError("DB2FS jobs are used but no filecatalog connection set.")
        return db2fs_to_activities(job, id_to_ls, fc_ls)


def execsql_to_activities(
    job: meta.ExecSQLJob, id_to_ls: dict[uuid.UUID, LinkedServiceBase]
) -> packages.ExecSQLPackage:
    """Transforms an ExecSQL job into a collection of adf
    activities.

    Args:
        job (meta.ExecSQLJob): _description_
        id_to_ls (dict[str, LinkedServiceBase]): _description_

    Returns:
        packages.ExecSQLPackage: _description_
    """
    sink_ls = id_to_ls[job.connection_id]
    if not isinstance(
        sink_ls,
        (
            linked_services.AzureSqlLinkedService,
            linked_services.AzureSynapseAnalyticsLinkedService,
            linked_services.SnowflakeLinkedService,
        ),
    ):
        raise NotImplementedError
    exec_activity = packages.ExecSQLPackage(
        job=job,
        description=job.description,
        linked_service=sink_ls,
        stored_procedure_identifier=job.get_procedure_identifier(),
    )
    logger.debug("Activity for %s created", job.name)
    return exec_activity


def fs2db_to_activities(
    job: meta.FS2DB,
    id_to_ls: dict[uuid.UUID, LinkedServiceBase],
    fc_ls: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.SnowflakeLinkedService,
    exec_package: packages.ExecSQLPackage | None = None,
) -> packages.FS2DBPackage:
    source_ls = id_to_ls[job.source_connection_id]
    sink_ls = id_to_ls[job.sink_connection_id]
    if not isinstance(source_ls, linked_services.AzureBlobStorageLinkedService):
        raise NotImplementedError
    if not isinstance(
        sink_ls,
        (
            linked_services.AzureSqlLinkedService,
            linked_services.AzureSynapseAnalyticsLinkedService,
            linked_services.SnowflakeLinkedService,
        ),
    ):
        raise NotImplementedError
    step = packages.FS2DBPackage(
        job=job,
        source_ls=source_ls,
        sink_ls=sink_ls,
        fc_ls=fc_ls,
        exec_job=exec_package,
    )
    logger.debug("Activity for %s created", job.name)
    return step


def db2fs_to_activities(
    job: meta.DB2FS,
    id_to_ls: dict[uuid.UUID, LinkedServiceBase],
    fc_ls: linked_services.AzureSqlLinkedService
    | linked_services.AzureSynapseAnalyticsLinkedService
    | linked_services.SnowflakeLinkedService,
) -> packages.DB2FSPackage:
    source_ls = id_to_ls[job.source_connection_id]
    sink_ls = id_to_ls[job.sink_connection_id]
    if not isinstance(
        source_ls,
        (
            linked_services.AzureSqlLinkedService,
            linked_services.AzureSynapseAnalyticsLinkedService,
            linked_services.SnowflakeLinkedService,
            linked_services.OracleLinkedService,
            linked_services.SqlServerLinkedService,
            linked_services.DB2LinkedService,
            linked_services.PostgreSQLLinkedService,
            linked_services.AzurePostgreSQLLinkedService,
        ),
    ):
        raise NotImplementedError
    if not isinstance(sink_ls, linked_services.AzureBlobStorageLinkedService):
        raise NotImplementedError
    step = packages.DB2FSPackage(
        job=job,
        source_ls=source_ls,
        sink_ls=sink_ls,
        activity_description=job.description,
        sequence_column_name=job.sequence_column_name,
        ds_in_schema_name=job.source_table.schema_name,
        ds_in_table_name=job.source_table.name,
        act_in_reader_query=job.render_select_statement(),
        ds_out_sink_directory=job.rendered_folder_path,
        ds_out_sink_file_name=job.get_sink_file_name(),
        datasource_info_id=str(job.datasource_info_id),
        datasttype_id=str(job.ds_type.id),
        filestorage_id=str(job.sink_connection_id),
        fc_ls=fc_ls,
    )
    logger.debug("Activity for %s created", job.name)
    return step
