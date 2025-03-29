import logging

import cloecore.utils.exceptions as custom_errors
import cloecore.utils.model as meta
import cloecore.utils.reader.model as mreader

logger = logging.getLogger(__name__)


def read_simple_pipe_file(
    errors: custom_errors.ModelerError,
    models: dict[str, list],
    pipes: meta.Pipes,
    databases: meta.Databases,
) -> meta.Pipes:
    new_pipes: list[meta.SimplePipe] = []
    raw_model_json = models.pop("modeler.sp", [])
    for raw_sp in raw_model_json:
        pipe = mreader.read_raw_simple_pipe(
            raw_sp,
            databases=databases,
        )
        if isinstance(pipe, custom_errors.SimplePipeError):
            errors.simple_pipe_error.append(pipe)
        else:
            new_pipes.append(pipe)
    pipes.pipes += new_pipes
    return pipes
