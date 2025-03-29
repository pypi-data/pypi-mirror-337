import logging

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta
import cloecore.utils.model.modeler as modeler
import cloecore.utils.model.modeler.powerpipe as pp
import cloecore.utils.reader.model as mreader

logger = logging.getLogger(__name__)


def read_powerpipe_file(
    errors: custom_errors.ModelerError,
    models: dict[str, list],
    pipes: meta.Pipes,
    tenants: meta.Tenants,
    engine_templates: modeler.SQLTemplates,
    sql_templates: modeler.SQLTemplates,
    databases: meta.Databases,
    conversion_templates: modeler.ConversionTemplates,
) -> meta.Pipes:
    new_pipes: list[pp.PowerPipe] = []
    raw_model_json = models.pop("modeler.pp", [])
    for raw_pp in raw_model_json:
        pipe = mreader.read_raw_powerpipe(
            raw_pp,
            databases=databases,
            engine_templates=engine_templates,
            tenants=tenants,
            sql_templates=sql_templates,
            conversion_templates=conversion_templates,
        )
        if isinstance(pipe, custom_errors.PowerPipeError):
            errors.power_pipe_error.append(pipe)
        else:
            new_pipes.append(pipe)
    pipes.pipes += new_pipes
    return pipes
