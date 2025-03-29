import logging
import pathlib

import cloecore.sql_orchestrator.batches as libatch
import cloecore.utils.model as meta
import cloecore.utils.SQL as sql
from cloecore.utils import reader, writer

logger = logging.getLogger(__name__)


def deploy(
    input_model_path: pathlib.Path,
    output_sql_path: pathlib.Path,
    output_single: bool,
    output_sql_transaction_separator: str,
    transaction_based_exec_sql: bool,
) -> None:
    files_found = reader.read_models_from_disk(reader.find_files(input_model_path))
    (
        s_errors,
        id_to_table,
        id_to_ds_type,
        id_to_conn,
        id_to_ds_info,
    ) = reader.read_jobs_support_files(files_found)
    s_errors.log_report()
    j_errors, jobs = reader.read_jobs_base_files(
        models=files_found,
        id_to_conn=id_to_conn,
        ds_types=id_to_ds_type,
        databases=id_to_table,
        ds_infos=id_to_ds_info,
    )
    j_errors.log_report()
    b_errors, batches = reader.read_orchestration_base_files(
        models=files_found,
    )
    b_errors.log_report()
    sql_batches, sql_batchsteps, sql_batchstep_dependencies = libatch.create_batch(
        batches
    )
    output_dict = {}
    output_dict["batch"] = sql.insert_table_sql(
        sql_batches,
        "cloe_orc",
        "batch",
        truncate_before_insert=True,
        identity_insert=True,
        output_sql_transaction_separator=output_sql_transaction_separator,
    )
    output_dict["batchsteps"] = sql.insert_table_sql(
        sql_batchsteps,
        "cloe_orc",
        "batchsteps",
        truncate_before_insert=True,
        output_sql_transaction_separator=output_sql_transaction_separator,
    )
    output_dict["batchstep_dependencies"] = sql.insert_table_sql(
        sql_batchstep_dependencies,
        "cloe_orc",
        "batchstep_dependencies",
        truncate_before_insert=True,
        output_sql_transaction_separator=output_sql_transaction_separator,
    )
    used_job_ids = [
        batchstep.job_id for batch in batches for batchstep in batch.batchsteps
    ]
    used_exec_sql_jobs = [
        job for job in jobs.get_exec_sql_jobs() if job.id in used_job_ids
    ]
    output_dict |= sql.create_stored_procedure_script(
        used_exec_sql_jobs, transaction_based_exec_sql
    )
    job_to_proc = [
        {"fk_job_id": job.id, "procedure_name": job.get_procedure_identifier()}
        for job in jobs.jobs
        if isinstance(job, meta.ExecSQLJob)
    ]
    output_dict["job_to_proc"] = sql.insert_table_sql(
        job_to_proc,
        "cloe_orc",
        "job_to_proc",
        truncate_before_insert=True,
        output_sql_transaction_separator=output_sql_transaction_separator,
    )
    if output_single:
        complete_file = ""
        for k, v in output_dict.items():
            complete_file += v
        writer.write_string_to_disk(
            complete_file, output_sql_path / "sql_orchestrator_configuration.sql"
        )
    else:
        for k, v in output_dict.items():
            v = f"{v}\n"
            writer.write_string_to_disk(v, output_sql_path / f"{k}.sql")
