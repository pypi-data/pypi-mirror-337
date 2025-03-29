import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def read_ds_type_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> meta.DatasetTypes:
    ds_types: list[meta.DatasetType] = []
    raw_model_json = models.pop("repository.ds_datasettype", [])
    for raw_ds_type in raw_model_json:
        try:
            ds_type = meta.DatasetType(**raw_ds_type)
            ds_types.append(ds_type)
        except ValidationError as error:
            error_name = f"{raw_ds_type.get('name', str(uuid.uuid4()))}"
            errors.ds_types[error_name] = error
    try:
        return meta.DatasetTypes(dataset_types=ds_types)
    except ValidationError as error:
        errors.ds_types["DatasetTypes"] = error
        return meta.DatasetTypes()
