import pathlib
from typing import Literal

import click

import cloecore.to_sql as tosql


@click.command()
@click.argument(
    "input-model-path",
    type=click.Path(exists=True, resolve_path=True, path_type=pathlib.Path),
)
@click.argument(
    "output-path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
)
@click.option(
    "--output-mode",
    required=False,
    default="sql_single",
    show_default=True,
    help=(
        "The outputs modes configures if one file per pipe is written to"
        " disk(sql_multi) or just one big file(sql_single) with all pipes"
        " or a exec_job json (json_single)."
    ),
    type=click.Choice(["sql_single", "json_single"]),
)
@click.option(
    "--output-sql-language",
    required=False,
    default="snowsql",
    show_default=True,
    help="Output sql language.",
    type=click.Choice(["tsql", "snowsql"]),
)
@click.option(
    "--update-existing-exec-sql-jobs",
    default=False,
    is_flag=True,
    help="Update existing jobs.",
)
def gen_sql(
    input_model_path: pathlib.Path,
    output_path: pathlib.Path,
    output_mode: Literal["sql_single", "json_single"],
    output_sql_language: Literal["tsql", "snowsql"],
    update_existing_exec_sql_jobs: bool,
) -> None:
    """This script reads in a cloe model. It then generates
    sql procedures and dq views and/or a exec_sql json."""
    tosql.deploy(
        input_model_path,
        output_path,
        output_mode,
        output_sql_language,
        update_existing_exec_sql_jobs,
    )
