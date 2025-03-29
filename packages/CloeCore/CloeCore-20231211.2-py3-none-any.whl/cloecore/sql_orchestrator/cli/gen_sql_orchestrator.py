import pathlib

import click

import cloecore.sql_orchestrator as tolite


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
    default="single",
    show_default=True,
    type=click.Choice(["single", "multi"]),
    help=(
        "The sql outputs modes configures if one file per source is written to"
        " disk(multi) or just one big file(single) with all statements."
    ),
)
@click.option(
    "--output-sql-transaction-separator",
    required=False,
    default=";\nGO",
    help="The separator to put between insert and create statements.",
)
@click.option(
    "--transaction-based-exec-sql",
    default=False,
    is_flag=True,
    help="Run each query of ExecSQL jobs in its own transaction.",
)
def gen_sql_orchestrator(
    input_model_path: pathlib.Path,
    output_path: pathlib.Path,
    output_mode: str,
    output_sql_transaction_separator: str,
    transaction_based_exec_sql: bool,
) -> None:
    """This script reads in a cloe model. It then generates
    insert statements for the orchestrator lite
    and corresponding sql stored procedures."""
    tolite.deploy(
        input_model_path,
        output_path,
        output_mode == "single",
        output_sql_transaction_separator,
        transaction_based_exec_sql,
    )
