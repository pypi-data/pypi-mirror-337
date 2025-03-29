import logging
import uuid

from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


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


class ConversionTemplates(BaseModel):
    """Base class for loading CLOE ConversionTemplate model objects."""

    conversiontemplates: list[ConversionTemplate] = Field(default={}, exclude=True)
    conversiontemplate_cache: dict[str, ConversionTemplate] = Field({}, exclude=True)

    @validator("conversiontemplates")
    def child_uniqueness_check(cls, value: list[ConversionTemplate]):
        validators.find_non_unique(value, "output_type")
        return value

    def get_template_by_id(self, template_id: str) -> ConversionTemplate:
        if len(self.conversiontemplate_cache) < 1:
            self.conversiontemplate_cache = {
                template.output_type: template for template in self.conversiontemplates
            }
        return self.conversiontemplate_cache[template_id]

    def check_if_conversiontemplate_exists_by_id(self, templates_id: uuid.UUID) -> bool:
        if len(self.conversiontemplate_cache) < 1:
            self.conversiontemplate_cache = {
                template.output_type: template for template in self.conversiontemplates
            }
        return templates_id in self.conversiontemplate_cache
