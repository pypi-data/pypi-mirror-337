import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model.jobs.connections as conn
import cloecore.utils.model.jobs.exec_sql as esql


def read_raw_exec_sql(
    raw_exec_sql: dict,
    connections: conn.Connections,
) -> esql.ExecSQLJob | custom_errors.ExecSQLError:
    errors = custom_errors.ExecSQLError(raw_exec_sql.get("name", str(uuid.uuid4())))
    queries = []
    for raw_runt in raw_exec_sql.pop("queries", []):
        try:
            runt = esql.ExecSQLRuntime(**raw_runt)
            queries.append(runt)
        except ValidationError as error:
            error_name = f"runt_{raw_runt.get('exec_order', str(uuid.uuid4()))}"
            errors.queries[error_name] = error
    try:
        exec_sql = esql.ExecSQLJob(
            **raw_exec_sql, queries=queries, connections=connections
        )
    except ValidationError as error:
        errors.base = error
    return errors if errors.is_charged else exec_sql
