import logging

import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def create_stored_procedure_script(
    jobs: list[meta.ExecSQL], is_transaction: bool = False
) -> dict[str, str]:
    proc_per_source: dict[str, str] = {}
    for job in jobs:
        if job.sink_connection.get_short_id() in proc_per_source:
            proc_per_source[
                job.sink_connection.get_short_id()
            ] += job.get_procedure_create_query(is_transaction)
        else:
            proc_per_source[
                job.sink_connection.get_short_id()
            ] = job.get_procedure_create_query(is_transaction)
        logger.debug("%s created", job.get_procedure_name())
    return proc_per_source
