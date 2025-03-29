import logging
import uuid

from pydantic import ValidationError

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model.modeler as modeler

logger = logging.getLogger(__name__)


def read_engine_template_file(
    errors: custom_errors.SupportError,
    models: dict[str, list],
) -> modeler.SQLTemplates:
    sql_templates: list[modeler.SQLTemplate] = []
    raw_model_json = models.pop("modeler.engine_templates", [])
    for raw_engine_template in raw_model_json:
        try:
            sql_template = modeler.SQLTemplate(**raw_engine_template)
            sql_templates.append(sql_template)
        except ValidationError as error:
            error_name = f"{raw_engine_template.get('name', str(uuid.uuid4()))}"
            errors.engine_templates[error_name] = error
    try:
        return modeler.SQLTemplates(sql_templates=sql_templates)
    except ValidationError as error:
        errors.engine_templates["EngineTemplates"] = error
        return modeler.SQLTemplates()
