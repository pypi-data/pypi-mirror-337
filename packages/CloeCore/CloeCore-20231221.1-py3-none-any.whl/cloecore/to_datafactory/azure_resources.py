import logging
import uuid
from typing import cast

import cloecore.to_datafactory.arm.general as arm
import cloecore.to_datafactory.factory as buildfactory
import cloecore.utils.model as meta
import cloecore.utils.SQL as sql
from cloecore.to_datafactory.arm.datafactory import base

logger = logging.getLogger(__name__)


def build_factory(
    batches: list[meta.Batch],
    jobs: dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob],
    connections: dict[uuid.UUID, meta.Connection],
    transaction_based_exec_sql: bool,
) -> tuple[dict[str, str | dict | list], dict[str, str | dict], dict[str, str]]:
    kv_ls, fc_ls, conn_id_to_ls = buildfactory.model_conn_to_linked_service(connections)
    logger.info("%s Connections created", len(conn_id_to_ls))
    datasets, pipelines, trigger = buildfactory.create_pipelines(
        batches,
        jobs,
        fc_ls,
        conn_id_to_ls,
    )
    logger.info("%s Pipelines created", len(pipelines))
    proc_per_source = sql.create_stored_procedure_script(
        [job for job in jobs.values() if isinstance(job, meta.ExecSQLJob)],
        transaction_based_exec_sql,
    )
    logger.info("Stored procedures created")
    factory = base.Factory()
    logger.info("Factory template created")
    all_res = (
        [factory]
        + [kv_ls]
        + list(conn_id_to_ls.values())
        + datasets
        + pipelines
        + trigger
    )
    template = arm.Template(cast(list[arm.ARMBase], all_res))
    return template.to_arm_template(), template.to_arm_parameter_file(), proc_per_source
