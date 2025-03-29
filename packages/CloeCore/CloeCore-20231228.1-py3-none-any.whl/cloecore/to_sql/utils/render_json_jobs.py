import logging
import pathlib
import uuid

import cloecore.to_sql.model.modeler as tmodeler
import cloecore.utils.model as meta
import cloecore.utils.reader as reader
from cloecore.to_sql.model import modeler
from cloecore.utils import exceptions
from cloecore.utils.model.jobs import exec_sql

logger = logging.getLogger(__name__)


def json_job_merger(
    jobs: meta.Jobs,
    existing_jobs: meta.Jobs,
) -> meta.Jobs:
    old_jobs = {job.id: job for job in existing_jobs.get_exec_sql_jobs()}
    for job in jobs.get_exec_sql_jobs():
        if job.id in old_jobs and old_jobs[job.id].queries != job.queries:
            old_jobs[job.id].queries = job.queries
        else:
            old_jobs[job.id] = job
    return meta.Jobs(jobs=[job for job in old_jobs.values()])


def existing_jobs_load(
    output_path: pathlib.Path,
    all_files: list[pathlib.Path],
    files_found: dict[str, list],
) -> tuple[meta.Jobs, pathlib.Path]:
    filename = "exec_sql.json"
    if prev_path := reader.find_model_object_path(all_files, "jobs.exec_sql"):
        filename = pathlib.Path(prev_path).name
    output_path = output_path / filename
    s_errors, connections = reader.read_exec_sql_jobs_support_files(files_found)
    s_errors.log_report()
    j_error = exceptions.JobError()
    jobs = meta.Jobs()
    existing_jobs = reader.read_exec_sql_file(j_error, files_found, jobs, connections)
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
        existing_jobs = meta.Jobs()
        output_path = output_path / "exec_sql.json"
    jobs: list[meta.DB2FS | meta.FS2DB | meta.ExecSQLJob] = []
    for pipe in pipes:
        output_key = pipe.job_id or uuid.uuid4()
        if isinstance(pipe, modeler.PowerPipeGenerator):
            query = pipe.gen_exec_sql_query(targettype_to_conversion)
        elif isinstance(pipe, modeler.SimplePipeGenerator):
            query = pipe.gen_job()
        else:
            raise ValueError("Unknown job type.")
        exec_job = exec_sql.ExecSQLJob.construct(
            id=output_key,
            name=pipe.name,
            queries=query,
            connection_id=uuid.UUID(int=0),
        )
        jobs.append(exec_job)
    new_jobs = json_job_merger(meta.Jobs(jobs=jobs), existing_jobs)
    return output_path, exec_sql.ExecSQLJobs(
        model_content=new_jobs.get_exec_sql_jobs()
    ).json(indent=4, by_alias=True, exclude_none=True)
