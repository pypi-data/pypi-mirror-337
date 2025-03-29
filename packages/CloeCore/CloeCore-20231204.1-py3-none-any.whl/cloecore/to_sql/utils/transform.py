from cloecore.to_sql import model
from cloecore.to_sql.model.modeler import (
    ConversionTemplateGenerator,
    PowerPipeGenerator,
    SimplePipeGenerator,
)
from cloecore.to_sql.sql.sql_syntax import SQLSyntax
from cloecore.utils.model import modeler


def transform_pipes(
    pipes: list[modeler.SimplePipe | modeler.PowerPipe],
    sql_syntax: SQLSyntax,
    engine_templates: model.EngineTemplates,
) -> list[PowerPipeGenerator | SimplePipeGenerator]:
    """Transform powerpipes and simplepipes to Generator classes.

    Args:
        pipes (list): _description_
        sql_syntax (SQLSyntax): _description_

    Returns:
        list[PowerPipeGenerator | SimplePipeGenerator]: _description_
    """
    trans_pipes: list[PowerPipeGenerator | SimplePipeGenerator] = []
    for pipe in pipes:
        if isinstance(pipe, modeler.PowerPipe):
            trans_pipes.append(PowerPipeGenerator(pipe, sql_syntax))
        if isinstance(pipe, modeler.SimplePipe):
            trans_pipes.append(SimplePipeGenerator(pipe))
    return trans_pipes


def transform_common(
    commons: dict, sql_syntax: SQLSyntax
) -> dict[str, ConversionTemplateGenerator]:
    """Transforms common templates.

    Args:
        commons (dict): _description_
        sql_syntax (SQLSyntax): _description_

    Returns:
        list[ConversionTemplateGenerator, SQLTemplate]: _description_
    """
    for k, temp in commons.items():
        if isinstance(temp, modeler.ConversionTemplate):
            commons[k] = ConversionTemplateGenerator(temp, sql_syntax)
    return commons
