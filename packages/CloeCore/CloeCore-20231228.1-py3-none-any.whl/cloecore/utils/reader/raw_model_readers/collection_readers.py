import logging
from typing import Tuple

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta
import cloecore.utils.model.modeler as modeler
import cloecore.utils.reader.model as mreader
from cloecore.utils.reader import raw_model_readers

logger = logging.getLogger(__name__)


def read_jobs_support_files(
    models: dict[str, list],
) -> Tuple[
    custom_errors.SupportError,
    meta.Databases,
    meta.DatasetTypes,
    meta.Connections,
    meta.DataSourceInfos,
]:
    errors = custom_errors.SupportError()
    tables = raw_model_readers.read_database_file(errors, models)
    tenants = raw_model_readers.read_tenant_file(errors, models)
    ds_types = raw_model_readers.read_ds_type_file(errors, models)
    sourcesystems = raw_model_readers.read_sourcesystem_file(errors, models)
    id_to_conn = raw_model_readers.read_connection_file(errors, models)
    ds_infos = raw_model_readers.read_ds_info_file(
        errors, models, tenants, sourcesystems
    )
    return (errors, tables, ds_types, id_to_conn, ds_infos)


def read_orchestration_base_files(
    models: dict[str, list],
) -> Tuple[custom_errors.OrchestrationError, list[meta.Batch]]:
    batches: list[meta.Batch] = []
    errors = custom_errors.OrchestrationError()
    raw_model_json = models.pop("batches", [])
    for raw_batch in raw_model_json:
        batch = mreader.read_raw_batch(
            raw_batch=raw_batch,
        )
        if isinstance(batch, custom_errors.BatchError):
            errors.batch_errors.append(batch)
        else:
            batches.append(batch)
    return errors, batches


def read_modeler_support_files(
    models: dict[str, list],
) -> Tuple[
    custom_errors.SupportError,
    modeler.SQLTemplates,
    modeler.SQLTemplates,
    modeler.DatatypeTemplates,
    modeler.ConversionTemplates,
    meta.Databases,
    meta.Tenants,
]:
    errors = custom_errors.SupportError()
    databases = raw_model_readers.read_database_file(errors, models)
    id_to_sqltemplate = raw_model_readers.read_sql_template_file(errors, models)
    id_to_enginetemplate = raw_model_readers.read_engine_template_file(errors, models)
    sourcetype_to_datatype = raw_model_readers.read_datatype_file(errors, models)
    tenants = raw_model_readers.read_tenant_file(errors, models)
    targettype_to_conversion = raw_model_readers.read_conversion_file(errors, models)
    return (
        errors,
        id_to_sqltemplate,
        id_to_enginetemplate,
        sourcetype_to_datatype,
        targettype_to_conversion,
        databases,
        tenants,
    )


def read_exec_sql_jobs_support_files(
    models: dict[str, list],
) -> Tuple[custom_errors.SupportError, meta.Connections]:
    errors = custom_errors.SupportError()
    id_to_conn = raw_model_readers.read_connection_file(errors, models)
    return errors, id_to_conn


def read_modeler_base_files(
    models: dict[str, list],
    tenants: meta.Tenants,
    engine_templates: modeler.SQLTemplates,
    sql_templates: modeler.SQLTemplates,
    databases: meta.Databases,
    conversion_templates: modeler.ConversionTemplates,
) -> Tuple[custom_errors.ModelerError, modeler.Pipes]:
    pipes = modeler.Pipes()
    errors = custom_errors.ModelerError()
    pipes = raw_model_readers.read_powerpipe_file(
        errors,
        models,
        pipes,
        tenants,
        engine_templates,
        sql_templates,
        databases,
        conversion_templates,
    )
    pipes = raw_model_readers.read_simple_pipe_file(errors, models, pipes, databases)
    return errors, pipes


def read_jobs_base_files(
    models: dict[str, list],
    id_to_conn: meta.Connections,
    ds_types: meta.DatasetTypes,
    databases: meta.Databases,
    ds_infos: meta.DataSourceInfos,
) -> Tuple[
    custom_errors.JobError,
    meta.Jobs,
]:
    jobs = meta.Jobs()
    errors = custom_errors.JobError()
    jobs = raw_model_readers.read_exec_sql_file(errors, models, jobs, id_to_conn)
    jobs = raw_model_readers.read_fs2db_file(
        errors,
        models,
        jobs,
        id_to_conn,
        ds_types,
        databases,
    )
    jobs = raw_model_readers.read_db2fs_file(
        errors, models, jobs, id_to_conn, ds_types, databases, ds_infos
    )
    return errors, jobs
