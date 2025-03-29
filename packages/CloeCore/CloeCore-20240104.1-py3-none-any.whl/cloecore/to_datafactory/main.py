import logging
import pathlib

import cloecore.to_datafactory.azure_resources as azure_res
import cloecore.utils.model as meta
import cloecore.utils.reader as reader
import cloecore.utils.writer as writer

logger = logging.getLogger(__name__)


def deploy(
    input_model_path: pathlib.Path,
    output_arm_path: pathlib.Path,
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
    factory_template, factory_params, sql_procs = azure_res.build_factory(
        batches.batches, jobs_c, connections, transaction_based_exec_sql
    )
    writer.write_dict_to_disk_json(
        factory_template, output_arm_path / "factory_template.json"
    )
    writer.write_dict_to_disk_json(
        factory_params, output_arm_path / "factory_parameters.json"
    )
    for k, v in sql_procs.items():
        writer.write_string_to_disk(v, output_sql_path / f"stored_procedures{k}.sql")
