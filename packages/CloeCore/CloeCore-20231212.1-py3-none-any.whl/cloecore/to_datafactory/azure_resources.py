import logging
import uuid

import cloecore.utils.model as meta
import cloecore.utils.SQL as sql
from cloecore.to_datafactory import factory_objects, utils

logger = logging.getLogger(__name__)


def build_factory(
    batches: list[meta.Batch],
    jobs: dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob],
    transaction_based_exec_sql: bool,
) -> tuple[
    list[factory_objects.PipelineResource],
    list[factory_objects.Trigger],
    dict[str, str],
]:
    pipelines, triggers = utils.create_pipelines(
        batches,
        jobs,
    )
    logger.info("%s Pipelines created", len(pipelines))
    proc_per_source = sql.create_stored_procedure_script(
        [job for job in jobs.values() if isinstance(job, meta.ExecSQLJob)],
        transaction_based_exec_sql,
    )
    logger.info("Stored procedures created")
    logger.info("Factory template created")
    return pipelines, triggers, proc_per_source
