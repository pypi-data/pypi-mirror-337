import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta

logger = logging.getLogger(__name__)


def read_ds_info_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
    tenants: meta.Tenants,
    sourcesystems: meta.Sourcesystems,
) -> meta.DataSourceInfos:
    ds_infos: list[meta.DataSourceInfo] = []
    raw_model_json = models.pop("repository.ds_datasourceinfo", [])
    for raw_ds_info in raw_model_json:
        try:
            ds_info = meta.DataSourceInfo(
                **raw_ds_info, sourcesystems=sourcesystems, tenants=tenants
            )
            ds_infos.append(ds_info)
        except ValidationError as error:
            error_name = f"{raw_ds_info.get('object_description', str(uuid.uuid4()))}"
            errors.ds_infos[error_name] = error
    try:
        return meta.DataSourceInfos(datasourceinfos=ds_infos)
    except ValidationError as error:
        errors.ds_infos["DataSourceInfos"] = error
        return meta.DataSourceInfos()
