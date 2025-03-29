import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def read_sourcesystem_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> meta.Sourcesystems:
    sourcesystems: list[meta.Sourcesystem] = []
    raw_model_json = models.pop("repository.ds_sourcesystem", [])
    for raw_ss in raw_model_json:
        try:
            sourcesystem = meta.Sourcesystem(**raw_ss)
            sourcesystems.append(sourcesystem)
        except ValidationError as error:
            error_name = f"{raw_ss.get('name', str(uuid.uuid4()))}"
            errors.sourcesystems[error_name] = error
    try:
        return meta.Sourcesystems(sourcesystems=sourcesystems)
    except ValidationError as error:
        errors.sourcesystems["Sourcesystems"] = error
        return meta.Sourcesystems()
