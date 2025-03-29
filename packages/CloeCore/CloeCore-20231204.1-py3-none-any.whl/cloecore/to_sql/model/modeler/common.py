from jinja2 import Template

from cloecore.to_sql.sql.sql_syntax import SQLSyntax
from cloecore.utils.model.modeler.common import ConversionTemplate


class ConversionTemplateGenerator:
    """Base class for working with conversion templates
    in the to_sql module.
    """

    def __init__(
        self, conversiontemplate: ConversionTemplate, sql_syntax: SQLSyntax
    ) -> None:
        self.output_type = conversiontemplate.output_type
        self.convert_template = conversiontemplate.convert_template
        self.on_convert_error_default_value = (
            conversiontemplate.on_convert_error_default_value
        )
        self.sql_syntax = sql_syntax

    def get_conversion_function_string(self, column_name: str) -> str:
        return self.convert_template.render(column_name=column_name, include_dq2=False)

    def get_dq_function_string(
        self,
        column_name: str,
        error_handling: bool,
        null_check_template: Template,
        error_handling_value: str | None = None,
    ) -> str:
        dq_function = self.convert_template.render(
            column_name=column_name, include_dq2=True
        )
        if error_handling:
            return self.sql_syntax.column_nullhandling(
                dq_function,
                null_check_template,
                error_handling_value or self.on_convert_error_default_value,
            )
        return dq_function
