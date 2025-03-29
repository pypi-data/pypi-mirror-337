import click

from cloecore.sql_orchestrator.cli import gen_sql_orchestrator
from cloecore.to_airflow.cli import gen_airflow
from cloecore.to_datafactory.cli import gen_datafactory
from cloecore.to_sql.cli import gen_ddls_from_db_model, gen_sql


@click.group()
def gen_cli() -> None:
    """Used as single interface for click to
    attach module cli's to.
    """
    pass


gen_cli.add_command(gen_airflow)
gen_cli.add_command(gen_datafactory)
gen_cli.add_command(gen_sql_orchestrator)
gen_cli.add_command(gen_sql)
gen_cli.add_command(gen_ddls_from_db_model)
