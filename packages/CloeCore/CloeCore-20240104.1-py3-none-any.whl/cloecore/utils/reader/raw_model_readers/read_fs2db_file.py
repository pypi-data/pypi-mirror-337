import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def read_fs2db_file(
    errors: custom_errors.JobError,
    models: dict[str, list],
    jobs: meta.Jobs,
    connections: meta.Connections,
    ds_types: meta.DatasetTypes,
    databases: meta.Databases,
) -> meta.Jobs:
    raw_model_json = models.pop("jobs.fs2db", [])
    new_jobs = []
    exec_sql_jobs = {job.id: job for job in jobs.get_exec_sql_jobs()}
    for raw_fs2db in raw_model_json:
        try:
            fs2db = meta.FS2DB(
                **raw_fs2db,
                connections=connections,
                exec_jobs=exec_sql_jobs,
                dataset_types=ds_types,
                tables=databases.tables,
            )
            new_jobs.append(fs2db)
        except ValidationError as error:
            error_name = f"{raw_fs2db.get('name', str(uuid.uuid4()))}"
            errors.fs_to_db[error_name] = error
    jobs.jobs += new_jobs
    return jobs
