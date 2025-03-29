import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model.repository.database as db


def read_raw_table(
    raw_table: dict, schema_name: str
) -> db.DatabaseTable | custom_errors.TableError:
    columns = []
    errors = custom_errors.TableError(raw_table.get("name", str(uuid.uuid4())))
    table_level = raw_table.get("level", "")
    for raw_column in raw_table.pop("columns", []):
        try:
            cm = db.TableColumn(**raw_column, table_level=table_level)
            columns.append(cm)
        except ValidationError as error:
            error_name = f"cm_{raw_column.get('name', str(uuid.uuid4()))}"
            errors.columns[error_name] = error
    try:
        table = db.DatabaseTable(
            **raw_table,
            schema_name=schema_name,
            columns=columns,
        )
    except ValidationError as error:
        errors.base = error
    return errors if errors.is_charged else table
