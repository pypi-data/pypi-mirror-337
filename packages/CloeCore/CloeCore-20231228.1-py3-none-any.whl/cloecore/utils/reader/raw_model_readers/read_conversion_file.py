import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model.modeler as modeler

logger = logging.getLogger(__name__)


def read_conversion_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> modeler.ConversionTemplates:
    conversions: list[modeler.ConversionTemplate] = []
    raw_model_json = models.pop("modeler.c_conversion", [])
    for raw_c_conversion in raw_model_json:
        try:
            conversion = modeler.ConversionTemplate(**raw_c_conversion)
            conversions.append(conversion)
        except ValidationError as error:
            error_name = f"{raw_c_conversion.get('output_type', str(uuid.uuid4()))}"
            errors.conversion_templates[error_name] = error
    try:
        return modeler.ConversionTemplates(conversiontemplates=conversions)
    except ValidationError as error:
        errors.conversion_templates["ConversionTemplates"] = error
        return modeler.ConversionTemplates()
