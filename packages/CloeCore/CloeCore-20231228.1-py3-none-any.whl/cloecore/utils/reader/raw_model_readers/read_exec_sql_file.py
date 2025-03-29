import logging

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta
import cloecore.utils.reader.model as mreader

logger = logging.getLogger(__name__)


def read_exec_sql_file(
    errors: custom_errors.JobError,
    models: dict[str, list],
    jobs: meta.Jobs,
    connections: meta.Connections,
) -> meta.Jobs:
    new_jobs = []
    raw_model_json = models.pop("jobs.exec_sql", [])
    for raw_execsql in raw_model_json:
        exec_sql = mreader.read_raw_exec_sql(
            raw_execsql,
            connections=connections,
        )
        if isinstance(exec_sql, custom_errors.ExecSQLError):
            errors.exec_sql.append(exec_sql)
        else:
            new_jobs.append(exec_sql)
    jobs.jobs += new_jobs
    return jobs
