from cloecore.to_sql.model.modeler import (
    ConversionTemplateGenerator,
    PowerPipeGenerator,
    SimplePipeGenerator,
)
from cloecore.to_sql.sql.sql_syntax import SQLSyntax
from cloecore.utils.model import modeler


def transform_pipes(
    pipes: modeler.Pipes,
    sql_syntax: SQLSyntax,
) -> list[PowerPipeGenerator | SimplePipeGenerator]:
    """Transform powerpipes and simplepipes to Generator classes.

    Args:
        pipes (list): _description_
        sql_syntax (SQLSyntax): _description_

    Returns:
        list[PowerPipeGenerator | SimplePipeGenerator]: _description_
    """
    trans_pipes: list[PowerPipeGenerator | SimplePipeGenerator] = []
    for pipe in pipes.pipes:
        if isinstance(pipe, modeler.PowerPipe):
            trans_pipes.append(PowerPipeGenerator(pipe, sql_syntax))
        if isinstance(pipe, modeler.SimplePipe):
            trans_pipes.append(SimplePipeGenerator(pipe))
    return trans_pipes


def transform_common(
    conversion_templates: modeler.ConversionTemplates, sql_syntax: SQLSyntax
) -> dict[str, ConversionTemplateGenerator]:
    """Transforms common templates.

    Args:
        commons (dict): _description_
        sql_syntax (SQLSyntax): _description_

    Returns:
        list[ConversionTemplateGenerator, SQLTemplate]: _description_
    """
    transformed_templates = {}
    for temp in conversion_templates.conversiontemplates:
        transformed_templates[temp.output_type] = ConversionTemplateGenerator(
            temp, sql_syntax
        )
    return transformed_templates
