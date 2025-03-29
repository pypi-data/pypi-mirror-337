import logging
import pathlib

from jinja2 import Environment, PackageLoader

import cloecore.utils.model as meta
import cloecore.utils.writer as writer
from cloecore.utils import templating_engine

logger = logging.getLogger(__name__)


def create_model_on_disk_from_db_model(
    output_path: pathlib.Path, databases: meta.Databases
) -> None:
    """
    Create DDL from database model.
    """
    package_loader = PackageLoader("cloecore.utils", "Templates")
    env_utils = templating_engine.get_jinja_env(package_loader)
    for database in databases.model_content:
        database_path = output_path / database.rendered_catalog_name
        writer.write_string_to_disk(
            database.get_ddl(),
            database_path / f"{database.rendered_catalog_name}.sql",
        )
        for schema in database.schemas:
            schema_path = database_path / "schemas" / schema.rendered_name
            writer.write_string_to_disk(
                schema.get_ddl(), schema_path / f"{schema.rendered_name}.sql"
            )
            tables_path = schema_path / "tables"
            for table in schema.tables:
                writer.write_string_to_disk(
                    table.get_ddl(env_utils), tables_path / f"{table.rendered_name}.sql"
                )


def create_script_from_db_model(databases: meta.Databases) -> str:
    """
    Create DDL from database model.
    """
    package_loader = PackageLoader("cloecore.utils", "Templates")
    env_utils = Environment(loader=package_loader)
    script = ""
    for database in databases.model_content:
        script += f"{database.get_ddl()}\n"
        for schema in database.schemas:
            script += f"{schema.get_ddl()}\n"
            for table in schema.tables:
                script += f"{table.get_ddl(env_utils)}\n"
    return script
