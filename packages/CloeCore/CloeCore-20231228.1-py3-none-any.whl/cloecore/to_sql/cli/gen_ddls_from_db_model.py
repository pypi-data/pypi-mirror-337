import pathlib

import click

from cloecore import to_sql


@click.command()
@click.argument(
    "input-model-path",
    type=click.Path(exists=True, resolve_path=True, path_type=pathlib.Path),
)
@click.argument(
    "output-folder-path",
    type=click.Path(
        exists=True, resolve_path=True, writable=True, path_type=pathlib.Path
    ),
)
@click.option(
    "--mode",
    default="single",
    type=click.Choice(["single", "multi"]),
    help=(
        "The mode of the DDL creation. The options are 'single' or 'multi'. When"
        " 'single' is selected the output is one file. When 'multi' is slected"
        " the output is multiple files that in a file hierarchy."
    ),
)
def gen_ddls_from_db_model(
    input_model_path: pathlib.Path,
    output_folder_path: pathlib.Path,
    mode: str,
) -> None:
    """
    Creates DDL's for a Snowflake Database model.
    """
    to_sql.write_ddls_to_disk(
        input_model_path=input_model_path,
        output_folder_path=output_folder_path,
        output_single=mode == "single",
    )
