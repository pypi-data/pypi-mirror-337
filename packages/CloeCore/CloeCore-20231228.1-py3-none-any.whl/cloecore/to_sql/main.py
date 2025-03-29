import logging
import pathlib
from typing import Literal

import cloecore.utils.reader as reader
import cloecore.utils.writer as writer
from cloecore.to_sql import model, utils
from cloecore.to_sql.sql.sql_syntax import SQLSyntax

logger = logging.getLogger(__name__)


def deploy(
    input_model_path: pathlib.Path,
    output_path: pathlib.Path,
    output_mode: Literal["sql_single", "json_single"],
    output_sql_system_type: Literal["tsql", "snowsql"],
    update_existing_exec_sql_jobs: bool,
) -> None:
    """Main entry for deploying to sql modeler.

    Args:
        input_model_path (str): _description_
        output_path (str): _description_
        output_mode (str): _description_
        output_sql_system_type (str): _description_
        existing_job_json_path (str | None, optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_
        ValueError: _description_
    """
    all_files = reader.find_files(input_model_path)
    files_found = reader.read_models_from_disk(all_files)
    (
        s_errors,
        id_to_sqltemplate,
        id_to_enginetemplate,
        sourcetype_to_datatype,
        targettype_to_conversion,
        databases,
        tenants,
    ) = reader.read_modeler_support_files(files_found)
    s_errors.log_report()
    m_errors, pipes = reader.read_modeler_base_files(
        models=files_found,
        tenants=tenants,
        engine_templates=id_to_enginetemplate,
        sql_templates=id_to_sqltemplate,
        databases=databases,
        conversion_templates=targettype_to_conversion,
    )
    m_errors.log_report()
    if output_sql_system_type == "tsql":
        template_package = "tsql"
        for table in databases.tables.values():
            table.tsql()
        output_sql_transaction_separator = ";\nGO"
    else:
        template_package = "snowsql"
        for table in databases.tables.values():
            table.snowflake()
        output_sql_transaction_separator = ";\n"
    engine_templates = model.EngineTemplates(template_package)
    engine_templates.merge_custom_templates(id_to_enginetemplate)
    sql_syntax = SQLSyntax(
        engine_templates,
        is_tsql=output_sql_system_type == "tsql",
        is_snowflake=output_sql_system_type == "snowsql",
    )
    trans_pipes = utils.transform_pipes(pipes, sql_syntax)
    trans_targettype_to_conversion = utils.transform_common(
        targettype_to_conversion, sql_syntax
    )
    if output_mode == "sql_single":
        content = utils.render_sql_script(
            trans_pipes,
            trans_targettype_to_conversion,
        )
        content_output_path = output_path / "rendered_pipe_queries.sql"
    else:
        content_output_path, content = utils.render_json_jobs(
            trans_pipes,
            trans_targettype_to_conversion,
            output_path,
            update_existing_exec_sql_jobs,
            all_files,
            files_found,
        )
    writer.write_string_to_disk(content, content_output_path)
    utils.deploy_dq_views(trans_pipes, output_path, output_sql_transaction_separator)


def write_ddls_to_disk(
    input_model_path: pathlib.Path,
    output_folder_path: pathlib.Path,
    output_single: bool,
) -> None:
    """
    Creates DDL's for a Snowflake Database model.
    """
    all_files = reader.find_files(input_model_path)
    files_found = reader.read_models_from_disk(all_files)
    (
        s_errors,
        id_to_sqltemplate,
        id_to_enginetemplate,
        sourcetype_to_datatype,
        targettype_to_conversion,
        databases,
        tenants,
    ) = reader.read_modeler_support_files(files_found)
    if output_single:
        content = utils.create_script_from_db_model(databases)
        writer.write_string_to_disk(content, output_folder_path / "cloe_ddls.sql")
    else:
        utils.create_model_on_disk_from_db_model(output_folder_path, databases)
