import logging
import pathlib
import uuid

import cloecore.to_sql.model.modeler as tmodeler
import cloecore.utils.model as meta
import cloecore.utils.reader as reader
from cloecore.to_sql.model import modeler
from cloecore.utils import exceptions
from cloecore.utils.model.jobs import Exec_SQL

logger = logging.getLogger(__name__)


def json_job_merger(
    jobs: dict[uuid.UUID, Exec_SQL.ExecSQLJob],
    existing_jobs: dict[uuid.UUID, Exec_SQL.ExecSQLJob],
) -> dict[uuid.UUID, Exec_SQL.ExecSQLJob]:
    for id, job in jobs.items():
        if id in existing_jobs and existing_jobs[id].queries != job.queries:
            existing_jobs[id].queries = job.queries
        else:
            existing_jobs[id] = job
    return existing_jobs


def existing_jobs_load(
    output_path: pathlib.Path,
    all_files: list[pathlib.Path],
    files_found: dict[str, list],
) -> tuple[dict[uuid.UUID, meta.ExecSQLJob], pathlib.Path]:
    filename = "exec_sql.json"
    if prev_path := reader.find_model_object_path(all_files, "jobs.exec_sql"):
        filename = pathlib.Path(prev_path).name
    output_path = output_path / filename
    s_errors, id_to_conn = reader.read_exec_sql_jobs_support_files(files_found)
    s_errors.log_report()
    j_error = exceptions.JobError()
    existing_jobs = reader.read_exec_sql_file(j_error, files_found, id_to_conn)
    j_error.log_report()
    return existing_jobs, output_path


def render_json_jobs(
    pipes: list[tmodeler.SimplePipeGenerator | tmodeler.PowerPipeGenerator],
    targettype_to_conversion: dict[str, modeler.ConversionTemplateGenerator],
    output_path: pathlib.Path,
    update_existing_exec_sql_jobs: bool,
    all_files: list[pathlib.Path],
    files_found: dict[str, list],
) -> tuple[pathlib.Path, str]:
    """Sub entrypoint for to_sql main function for output_mode json.

    Args:
        pipes (list[tmodeler.SimplePipeGenerator, tmodeler.PowerPipeGenerator]):
        _description_
        targettype_to_conversion (dict[str, modeler.ConversionTemplateGenerator]):
        _description_
        output_path (str): _description_
        output_sql_transaction_separator (str | None, optional): _description_.
        Defaults to ";\nGO".
        existing_job_json_path (str | None, optional): _description_.
        Defaults to None.
    """
    if update_existing_exec_sql_jobs:
        existing_jobs, output_path = existing_jobs_load(
            output_path, all_files, files_found
        )
    else:
        existing_jobs = {}
        output_path = output_path / "exec_sql.json"
    jobs = {}
    for pipe in pipes:
        output_key = pipe.job_id or uuid.uuid4()
        if isinstance(pipe, modeler.PowerPipeGenerator):
            query = pipe.gen_exec_sql_query(targettype_to_conversion)
        elif isinstance(pipe, modeler.SimplePipeGenerator):
            query = pipe.gen_job()
        else:
            raise ValueError("Unknown job type.")
        exec_job = Exec_SQL.ExecSQLJob.construct(
            id=output_key,
            name=pipe.name,
            queries=query,
            connection_id=uuid.UUID(int=0),
        )
        jobs[output_key] = exec_job
    jobs = json_job_merger(jobs, existing_jobs)
    return output_path, Exec_SQL.ExecSQLJobs(model_content=list(jobs.values())).json(
        indent=4, by_alias=True, exclude_none=True
    )
