import uuid

import cloecore.to_sql.model.modeler as tmodeler
from cloecore.to_sql.model import modeler


def render_sql_script(
    pipes: list[tmodeler.SimplePipeGenerator | tmodeler.PowerPipeGenerator],
    target_type_to_conversion: dict[str, modeler.ConversionTemplateGenerator],
) -> str:
    """Sub entrypoint for to_sql main function for output_mode sql_*.

    Args:
        pipes (list[SimplePipeGenerator, PowerPipeGenerator]):
        _description_
        target_type_to_conversion (dict[str, modeler.ConversionTemplateGenerator]):
        _description_
        output_path (str): _description_
        output_mode (str | None, optional): _description_. Defaults to "sql_multi".
        output_sql_transaction_separator (str | None, optional):
        _description_. Defaults to "".
    """
    output: dict[uuid.UUID, str] = {}
    for pipe in pipes:
        output_key = pipe.job_id or uuid.uuid4()
        if isinstance(pipe, modeler.PowerPipeGenerator):
            output[output_key] = pipe.gen_script(target_type_to_conversion)
        elif isinstance(pipe, modeler.SimplePipeGenerator):
            output[output_key] = pipe.gen_script()
    rendered_pipe_queries = ""
    for name, out in output.items():
        rendered_pipe_queries += f"\n\n\n\n--NEXT PIPE STARTING {name}\n{out}"
    return rendered_pipe_queries
