import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def read_connection_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> meta.Connections:
    new_connections: list[meta.Connection] = []
    raw_model_json = models.pop("jobs.connections", [])
    for raw_conn in raw_model_json:
        try:
            conn = meta.Connection(**raw_conn)
            new_connections.append(conn)
        except ValidationError as error:
            error_name = f"{raw_conn.get('name', str(uuid.uuid4()))}"
            errors.connections[error_name] = error
    try:
        return meta.Connections(connections=new_connections)
    except ValidationError as error:
        errors.connections["Connections"] = error
        return meta.Connections()
