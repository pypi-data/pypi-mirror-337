import logging
import uuid
from typing import Tuple

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta
import cloecore.utils.model.modeler as modeler
import cloecore.utils.model.modeler.powerpipe as pp
import cloecore.utils.model.repository as rp
import cloecore.utils.reader.model as mreader

logger = logging.getLogger(__name__)


def read_database_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> meta.Databases:
    databases = meta.Databases(model_content=[])
    for raw_database in models.pop("repository.db_full_catalog", []):
        raw_schemas: list[dict] = raw_database.pop("schemas", [])
        database = meta.DatabaseDatabase(**raw_database)
        databases.model_content.append(database)
        for raw_schema in raw_schemas:
            raw_tables: list[dict] = raw_schema.pop("tables", [])
            schema = meta.DatabaseSchema(**raw_schema)
            database.schemas.append(schema)
            for raw_table in raw_tables:
                table = mreader.read_raw_table(
                    raw_table=raw_table,
                    schema_name=schema.name,
                )
                if isinstance(table, custom_errors.TableError):
                    errors.tables.append(table)
                else:
                    schema.tables.append(table)
    return databases


def read_tenant_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[uuid.UUID, meta.Tenant]:
    tenants: dict[uuid.UUID, meta.Tenant] = {}
    for raw_tenant in models.pop("repository.tenant", []):
        try:
            tenant = meta.Tenant(**raw_tenant)
            tenants[tenant.id] = tenant
        except ValidationError as error:
            error_name = f"{raw_tenant.get('name', str(uuid.uuid4()))}"
            errors.tenants[error_name] = error
    return tenants


def read_ds_type_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[uuid.UUID, meta.DatasetType]:
    ds_types: dict[uuid.UUID, meta.DatasetType] = {}
    for raw_ds_type in models.pop("repository.ds_datasettype", []):
        try:
            ds_type = meta.DatasetType(**raw_ds_type)
            ds_types[ds_type.id] = ds_type
        except ValidationError as error:
            error_name = f"{raw_ds_type.get('name', str(uuid.uuid4()))}"
            errors.ds_types[error_name] = error
    return ds_types


def read_sourcesystem_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[uuid.UUID, rp.Sourcesystem]:
    sourcesystems: dict[uuid.UUID, rp.Sourcesystem] = {}
    for raw_ss in models.pop("repository.ds_sourcesystem", []):
        try:
            sourcesystem = rp.Sourcesystem(**raw_ss)
            sourcesystems[sourcesystem.id] = sourcesystem
        except ValidationError as error:
            error_name = f"{raw_ss.get('name', str(uuid.uuid4()))}"
            errors.sourcesystems[error_name] = error
    return sourcesystems


def read_connection_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[uuid.UUID, meta.Connection]:
    id_to_conn: dict[uuid.UUID, meta.Connection] = {}
    for raw_conn in models.pop("jobs.connections", []):
        try:
            conn = meta.Connection(**raw_conn)
            id_to_conn[conn.id] = conn
        except ValidationError as error:
            error_name = f"{raw_conn.get('name', str(uuid.uuid4()))}"
            errors.connections[error_name] = error
    return id_to_conn


def read_ds_info_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
    tenants: dict[uuid.UUID, meta.Tenant],
    sourcesystems: dict[uuid.UUID, rp.Sourcesystem],
) -> dict[uuid.UUID, meta.DataSourceInfo]:
    ds_infos: dict[uuid.UUID, meta.DataSourceInfo] = {}
    for raw_ds_info in models.pop("repository.ds_datasourceinfo", []):
        try:
            ds_info = meta.DataSourceInfo(
                **raw_ds_info, sourcesystems=sourcesystems, tenants=tenants
            )
            ds_infos[ds_info.id] = ds_info
        except ValidationError as error:
            error_name = f"{raw_ds_info.get('object_description', str(uuid.uuid4()))}"
            errors.ds_infos[error_name] = error
    return ds_infos


def read_sql_template_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[int, modeler.SQLTemplate]:
    id_to_sqltemplate: dict[int, modeler.SQLTemplate] = {}
    for raw_c_template in models.pop("modeler.c_templates", []):
        try:
            sql_template = modeler.SQLTemplate(**raw_c_template)
            id_to_sqltemplate[sql_template.id] = sql_template
        except ValidationError as error:
            error_name = f"{raw_c_template.get('name', str(uuid.uuid4()))}"
            errors.sql_templates[error_name] = error
    return id_to_sqltemplate


def read_engine_template_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[int, modeler.SQLTemplate]:
    id_to_enginetemplate: dict[int, modeler.SQLTemplate] = {}
    for raw_engine_template in models.pop("modeler.engine_templates", []):
        try:
            sql_template = modeler.SQLTemplate(**raw_engine_template)
            id_to_enginetemplate[sql_template.id] = sql_template
        except ValidationError as error:
            error_name = f"{raw_engine_template.get('name', str(uuid.uuid4()))}"
            errors.engine_templates[error_name] = error
    return id_to_enginetemplate


def read_datatype_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[str, modeler.DatatypeTemplate]:
    sourcetype_to_datatype: dict[str, modeler.DatatypeTemplate] = {}
    for raw_c_datatype in models.pop("modeler.c_datatype", []):
        try:
            c_type = modeler.DatatypeTemplate(**raw_c_datatype)
            sourcetype_to_datatype[c_type.source_type] = c_type
        except ValidationError as error:
            error_name = f"{raw_c_datatype.get('source_type', str(uuid.uuid4()))}"
            errors.ds_types[error_name] = error
    return sourcetype_to_datatype


def read_conversion_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> dict[str, modeler.ConversionTemplate]:
    targettype_to_conversion: dict[str, modeler.ConversionTemplate] = {}
    for raw_c_conversion in models.pop("modeler.c_conversion", []):
        try:
            conversion = modeler.ConversionTemplate(**raw_c_conversion)
            targettype_to_conversion[conversion.output_type] = conversion
        except ValidationError as error:
            error_name = f"{raw_c_conversion.get('output_type', str(uuid.uuid4()))}"
            errors.conversion_templates[error_name] = error
    return targettype_to_conversion


def read_powerpipe_file(
    errors: custom_errors.ModelerError,
    models: dict[str, list],
    tenants: dict[uuid.UUID, rp.Tenant],
    engine_templates: dict[int, modeler.SQLTemplate],
    sql_templates: dict[int, modeler.SQLTemplate],
    databases: meta.Databases,
    conversion_templates: dict[str, modeler.ConversionTemplate],
) -> list[pp.PowerPipe]:
    pipes: list[pp.PowerPipe] = []
    for raw_pp in models.pop("modeler.pp", []):
        powerpipe = mreader.read_raw_powerpipe(
            raw_pp,
            databases=databases,
            engine_templates=engine_templates,
            tenants=tenants,
            sql_templates=sql_templates,
            conversion_templates=conversion_templates,
        )
        if isinstance(powerpipe, custom_errors.PowerPipeError):
            errors.power_pipe_error.append(powerpipe)
        else:
            pipes.append(powerpipe)
    return pipes


def read_simple_pipe_file(
    errors: custom_errors.ModelerError,
    models: dict[str, list],
    databases: meta.Databases,
) -> list[meta.SimplePipe]:
    pipes: list[meta.SimplePipe] = []
    for raw_sp in models.pop("modeler.sp", []):
        simple_pipe = mreader.read_raw_simple_pipe(
            raw_sp,
            databases=databases,
        )
        if isinstance(simple_pipe, custom_errors.SimplePipeError):
            errors.simple_pipe_error.append(simple_pipe)
        else:
            pipes.append(simple_pipe)
    return pipes


def read_exec_sql_file(
    errors: custom_errors.JobError,
    models: dict[str, list],
    id_to_conn: dict[uuid.UUID, meta.Connection],
) -> dict[uuid.UUID, meta.ExecSQLJob]:
    id_to_job = {}
    for raw_execsql in models.pop("jobs.exec_sql", []):
        exec_sql = mreader.read_raw_exec_sql(
            raw_execsql,
            connections=id_to_conn,
        )
        if isinstance(exec_sql, custom_errors.ExecSQLError):
            errors.exec_sql.append(exec_sql)
        else:
            id_to_job[exec_sql.id] = exec_sql
    return id_to_job


def read_fs2db_file(
    errors: custom_errors.JobError,
    models: dict[str, list],
    id_to_job: dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS],
    id_to_conn: dict[uuid.UUID, meta.Connection],
    exec_jobs: dict[uuid.UUID, meta.ExecSQLJob],
    ds_types: dict[uuid.UUID, meta.DatasetType],
    databases: meta.Databases,
) -> dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS]:
    for raw_fs2db in models.pop("jobs.fs2db", []):
        try:
            fs2db = meta.FS2DB(
                **raw_fs2db,
                connections=id_to_conn,
                exec_jobs=exec_jobs,
                dataset_types=ds_types,
                tables=databases.tables,
            )
            id_to_job[fs2db.id] = fs2db
        except ValidationError as error:
            error_name = f"{raw_fs2db.get('name', str(uuid.uuid4()))}"
            errors.fs_to_db[error_name] = error
    return id_to_job


def read_db2fs_file(
    errors: custom_errors.JobError,
    models: dict[str, list],
    id_to_job: dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS],
    id_to_conn: dict[uuid.UUID, meta.Connection],
    ds_types: dict[uuid.UUID, meta.DatasetType],
    databases: meta.Databases,
    ds_infos: dict[uuid.UUID, meta.DataSourceInfo],
) -> dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS]:
    for raw_db2fs in models.pop("jobs.db2fs", []):
        try:
            db2fs = meta.DB2FS(
                **raw_db2fs,
                connections=id_to_conn,
                dataset_types=ds_types,
                tables=databases.tables,
                datasource_infos=ds_infos,
            )
            id_to_job[db2fs.id] = db2fs
        except ValidationError as error:
            error_name = f"{raw_db2fs.get('name', str(uuid.uuid4()))}"
            errors.db_to_fs[error_name] = error
    return id_to_job


def read_fs2fs_file(
    errors: custom_errors.JobError,
    models: dict[str, list],
    id_to_job: dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS],
    id_to_conn: dict[uuid.UUID, meta.Connection],
    ds_types: dict[uuid.UUID, meta.DatasetType],
    ds_infos: dict[uuid.UUID, meta.DataSourceInfo],
) -> dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS]:
    for raw_fs2fs in models.pop("jobs.fs2fs", []):
        try:
            fs2fs = meta.FS2FS(
                **raw_fs2fs,
                connections=id_to_conn,
                dataset_types=ds_types,
                datasource_infos=ds_infos,
            )
            id_to_job[fs2fs.id] = fs2fs
        except ValidationError as error:
            error_name = f"{raw_fs2fs.get('name', str(uuid.uuid4()))}"
            errors.fs_to_fs[error_name] = error
    return id_to_job


def read_jobs_support_files(
    models: dict[str, list],
) -> Tuple[
    custom_errors.SupportError,
    meta.Databases,
    dict[uuid.UUID, meta.DatasetType],
    dict[uuid.UUID, meta.Connection],
    dict[uuid.UUID, meta.DataSourceInfo],
]:
    errors = custom_errors.SupportError()
    tables = read_database_file(errors, models)
    tenants = read_tenant_file(errors, models)
    ds_types = read_ds_type_file(errors, models)
    sourcesystems = read_sourcesystem_file(errors, models)
    id_to_conn = read_connection_file(errors, models)
    ds_infos = read_ds_info_file(errors, models, tenants, sourcesystems)
    return (errors, tables, ds_types, id_to_conn, ds_infos)


def read_modeler_support_files(
    models: dict[str, list],
) -> Tuple[
    custom_errors.SupportError,
    dict[int, modeler.SQLTemplate],
    dict[int, modeler.SQLTemplate],
    dict[str, modeler.DatatypeTemplate],
    dict[str, modeler.ConversionTemplate],
    meta.Databases,
    dict[uuid.UUID, meta.Tenant],
]:
    errors = custom_errors.SupportError()
    databases = read_database_file(errors, models)
    id_to_sqltemplate = read_sql_template_file(errors, models)
    id_to_enginetemplate = read_engine_template_file(errors, models)
    sourcetype_to_datatype = read_datatype_file(errors, models)
    tenants = read_tenant_file(errors, models)
    targettype_to_conversion = read_conversion_file(errors, models)
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
) -> Tuple[custom_errors.SupportError, dict[uuid.UUID, meta.Connection]]:
    errors = custom_errors.SupportError()
    id_to_conn = read_connection_file(errors, models)
    return errors, id_to_conn


def read_orchestration_base_files(
    models: dict[str, list]
) -> Tuple[custom_errors.OrchestrationError, list[meta.Batch]]:
    batches: list[meta.Batch] = []
    errors = custom_errors.OrchestrationError()
    for raw_batch in models.pop("batches", []):
        batch = mreader.read_raw_batch(
            raw_batch=raw_batch,
        )
        if isinstance(batch, custom_errors.BatchError):
            errors.batch_errors.append(batch)
        else:
            batches.append(batch)
    return errors, batches


def read_modeler_base_files(
    models: dict[str, list],
    tenants: dict[uuid.UUID, rp.Tenant],
    engine_templates: dict[int, modeler.SQLTemplate],
    sql_templates: dict[int, modeler.SQLTemplate],
    databases: meta.Databases,
    conversion_templates: dict[str, modeler.ConversionTemplate],
) -> Tuple[custom_errors.ModelerError, list[pp.PowerPipe | modeler.SimplePipe]]:
    errors = custom_errors.ModelerError()
    pp_pipes = read_powerpipe_file(
        errors,
        models,
        tenants,
        engine_templates,
        sql_templates,
        databases,
        conversion_templates,
    )
    sp_pipes = read_simple_pipe_file(errors, models, databases)
    return errors, pp_pipes + sp_pipes


def read_jobs_base_files(
    models: dict[str, list],
    id_to_conn: dict[uuid.UUID, meta.Connection],
    ds_types: dict[uuid.UUID, meta.DatasetType],
    databases: meta.Databases,
    ds_infos: dict[uuid.UUID, meta.DataSourceInfo],
) -> Tuple[
    custom_errors.JobError,
    dict[uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS],
]:
    id_to_job: dict[
        uuid.UUID, meta.FS2DB | meta.DB2FS | meta.ExecSQLJob | meta.FS2FS
    ] = {}
    errors = custom_errors.JobError()
    id_to_exec_job = read_exec_sql_file(errors, models, id_to_conn)
    id_to_job |= id_to_exec_job
    id_to_job = read_fs2db_file(
        errors,
        models,
        id_to_job,
        id_to_conn,
        id_to_exec_job,
        ds_types,
        databases,
    )
    id_to_job = read_db2fs_file(
        errors, models, id_to_job, id_to_conn, ds_types, databases, ds_infos
    )
    id_to_job = read_fs2fs_file(
        errors, models, id_to_job, id_to_conn, ds_types, ds_infos
    )
    return errors, id_to_job
