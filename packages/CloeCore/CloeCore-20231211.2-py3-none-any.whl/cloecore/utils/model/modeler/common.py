import logging

from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, validator

from cloecore.utils import templating_engine

logger = logging.getLogger(__name__)


class SQLTemplate(BaseModel):
    """SQLTemplate metadata model base class"""

    id: int
    name: str
    template: str
    description: str | None = None

    @validator("template")
    def valid_jinja2_template(cls, value):
        try:
            templating_engine.get_jinja_env().from_string(value)
        except TemplateSyntaxError:
            raise ValueError("template is no valid jinja2 template")
        return value


class DatatypeTemplate(BaseModel):
    """DatatypeTemplate metadata model base class"""

    source_type: str
    parameter_template: Template

    class Config:
        arbitrary_types_allowed = True

    @validator("parameter_template", pre=True)
    def valid_jinja2_template(cls, value):
        try:
            return Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")


class ConversionTemplate(BaseModel):
    """ConversionTemplate metadata model base class"""

    output_type: str
    convert_template: Template
    on_convert_error_default_value: str

    class Config:
        arbitrary_types_allowed = True

    @validator("convert_template", pre=True)
    def valid_jinja2_template(cls, value):
        try:
            return Template(value)
        except TemplateSyntaxError:
            raise ValueError("is no valid jinja2 template")
