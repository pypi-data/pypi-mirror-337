import pathlib

import click

import cloecore.to_datafactory as tofactory


@click.command()
@click.argument(
    "input-model-path",
    type=click.Path(exists=True, resolve_path=True, path_type=pathlib.Path),
)
@click.argument(
    "output-arm-path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
)
@click.argument(
    "output-sql-path",
    type=click.Path(resolve_path=True, writable=True, path_type=pathlib.Path),
)
@click.option(
    "--transaction-based-exec-sql",
    default=False,
    is_flag=True,
    help="Run each query of ExecSQL jobs in its own transaction.",
)
def gen_datafactory(
    input_model_path: pathlib.Path,
    output_arm_path: pathlib.Path,
    output_sql_path: pathlib.Path,
    transaction_based_exec_sql: bool,
) -> None:
    """This script reads in a cloe model. It then generates
    azure Keyvault+Datafactory ARM templates and corresponding sql stored procedures."""
    tofactory.deploy(
        input_model_path, output_arm_path, output_sql_path, transaction_based_exec_sql
    )
