import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model.modeler as modeler

logger = logging.getLogger(__name__)


def read_datatype_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> modeler.DatatypeTemplates:
    datatypes: list[modeler.DatatypeTemplate] = []
    raw_model_json = models.pop("modeler.c_datatype", [])
    for raw_c_datatype in raw_model_json:
        try:
            c_type = modeler.DatatypeTemplate(**raw_c_datatype)
            datatypes.append(c_type)
        except ValidationError as error:
            error_name = f"{raw_c_datatype.get('source_type', str(uuid.uuid4()))}"
            errors.ds_types[error_name] = error
    try:
        return modeler.DatatypeTemplates(datatypetemplates=datatypes)
    except ValidationError as error:
        errors.ds_types["DatatypeTemplates"] = error
        return modeler.DatatypeTemplates()
