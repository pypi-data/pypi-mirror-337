import logging
import pathlib

import cloecore.to_airflow.airflow_build as airflow
import cloecore.utils.model as meta
import cloecore.utils.reader as reader
import cloecore.utils.SQL as sql
import cloecore.utils.writer as writer

logger = logging.getLogger(__name__)


def deploy(
    input_model_path: pathlib.Path,
    output_dag_path: pathlib.Path,
    output_sql_path: pathlib.Path,
    transaction_based_exec_sql: bool,
) -> None:
    files_found = reader.read_models_from_disk(reader.find_files(input_model_path))
    (
        s_errors,
        databases,
        dataset_types,
        connections,
        data_source_infos,
    ) = reader.read_jobs_support_files(files_found)
    s_errors.log_report()
    j_errors, jobs = reader.read_jobs_base_files(
        models=files_found,
        connections=connections,
        dataset_types=dataset_types,
        databases=databases,
        data_source_infos=data_source_infos,
    )
    j_errors.log_report()
    b_errors, batches = reader.read_orchestration_base_files(
        models=files_found,
    )
    b_errors.log_report()
    jobs_c = {}
    for job in jobs.jobs:
        if isinstance(job, (meta.FS2DB, meta.DB2FS, meta.ExecSQL)):
            jobs_c[job.id] = job
        else:
            raise NotImplementedError
    dags = airflow.create_dags(batches.batches, jobs_c, connections)
    proc_per_source = sql.create_stored_procedure_script(
        jobs.get_exec_sql_jobs(),
        transaction_based_exec_sql,
    )
    logger.info("Stored procedures created")
    for n, i in enumerate(dags):
        writer.write_string_to_disk(i.to_python(), output_dag_path / f"dags{n}.py")
    for k, v in proc_per_source.items():
        writer.write_string_to_disk(v, output_sql_path / f"{k}.sql")
