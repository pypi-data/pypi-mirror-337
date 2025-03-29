import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def read_db2fs_file(
    errors: custom_errors.JobError,
    models: dict[str, list],
    jobs: meta.Jobs,
    connections: meta.Connections,
    ds_types: meta.DatasetTypes,
    databases: meta.Databases,
    ds_infos: meta.DataSourceInfos,
) -> meta.Jobs:
    raw_model_json = models.pop("jobs.db2fs", [])
    new_jobs = []
    for raw_db2fs in raw_model_json:
        try:
            db2fs = meta.DB2FS(
                **raw_db2fs,
                connections=connections,
                dataset_types=ds_types,
                tables=databases.tables,
                datasource_infos=ds_infos,
            )
            new_jobs.append(db2fs)
        except ValidationError as error:
            error_name = f"{raw_db2fs.get('name', str(uuid.uuid4()))}"
            errors.db_to_fs[error_name] = error
    jobs.jobs += new_jobs
    return jobs
