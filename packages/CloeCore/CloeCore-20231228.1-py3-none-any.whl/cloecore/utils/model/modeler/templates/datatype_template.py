import logging
import uuid

from jinja2 import Template, TemplateSyntaxError
from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators

logger = logging.getLogger(__name__)


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


class DatatypeTemplates(BaseModel):
    """Base class for loading CLOE DatatypeTemplate model objects."""

    datatypetemplates: list[DatatypeTemplate] = Field(default={}, exclude=True)
    datatypetemplate_cache: dict[str, DatatypeTemplate] = Field({}, exclude=True)

    @validator("datatypetemplates")
    def child_uniqueness_check(cls, value: list[DatatypeTemplate]):
        validators.find_non_unique(value, "source_type")
        return value

    def get_template_by_id(self, template_id: str) -> DatatypeTemplate:
        if len(self.datatypetemplate_cache) < 1:
            self.datatypetemplate_cache = {
                template.source_type: template for template in self.datatypetemplates
            }
        return self.datatypetemplate_cache[template_id]

    def check_if_datatypetemplate_exists_by_id(self, templates_id: uuid.UUID) -> bool:
        if len(self.datatypetemplate_cache) < 1:
            self.datatypetemplate_cache = {
                template.source_type: template for template in self.datatypetemplates
            }
        return templates_id in self.datatypetemplate_cache
