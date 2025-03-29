import logging

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta
import cloecore.utils.reader.model as mreader

logger = logging.getLogger(__name__)


def read_database_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> meta.Databases:
    databases = []
    raw_model_json = models.pop("repository.db_full_catalog", [])
    for raw_database in raw_model_json:
        raw_schemas: list[dict] = raw_database.pop("schemas", [])
        database = meta.DatabaseDatabase(**raw_database)
        databases.append(database)
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
    try:
        return meta.Databases(model_content=databases)
    except ValidationError as error:
        errors.connections["Databases"] = error
        return meta.Databases(model_content=[])
