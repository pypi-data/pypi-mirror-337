import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model.modeler as sp
from cloecore.utils.model import repository


def read_raw_simple_pipe(
    raw_simple_pipe: dict,
    databases: repository.Databases,
) -> sp.SimplePipe | custom_errors.SimplePipeError:
    errors = custom_errors.SimplePipeError(
        raw_simple_pipe.get("name", str(uuid.uuid4()))
    )
    table_mappings = []
    for raw_tm in raw_simple_pipe.pop("table_mappings", []):
        try:
            tm = sp.SPTableMapping(**raw_tm, tables=databases.tables)
            table_mappings.append(tm)
        except ValidationError as error:
            error_name = f"tm_{raw_tm.get('sourcetable_id', str(uuid.uuid4()))}"
            errors.table_mapping[error_name] = error
    try:
        pipe = sp.SimplePipe(**raw_simple_pipe, table_mappings=table_mappings)
    except ValidationError as error:
        errors.base = error
    return errors if errors.is_charged else pipe
