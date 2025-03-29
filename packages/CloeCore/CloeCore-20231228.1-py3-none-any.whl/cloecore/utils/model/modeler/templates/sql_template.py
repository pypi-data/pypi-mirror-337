import logging
import uuid

from jinja2 import TemplateSyntaxError
from pydantic import BaseModel, Field, validator

from cloecore.utils import templating_engine
from cloecore.utils.model import validators

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


class SQLTemplates(BaseModel):
    """Base class for loading CLOE SQLTemplate model objects."""

    sqltemplates: list[SQLTemplate] = Field(default={}, exclude=True)
    sqltemplate_cache: dict[int, SQLTemplate] = Field({}, exclude=True)

    @validator("sqltemplates")
    def child_uniqueness_check(cls, value: list[SQLTemplate]):
        validators.find_non_unique(value, "name")
        return value

    def get_template_by_id(self, template_id: int) -> SQLTemplate:
        if len(self.sqltemplate_cache) < 1:
            self.sqltemplate_cache = {
                template.id: template for template in self.sqltemplates
            }
        return self.sqltemplate_cache[template_id]

    def check_if_sqltemplate_exists_by_id(self, templates_id: uuid.UUID) -> bool:
        if len(self.sqltemplate_cache) < 1:
            self.sqltemplate_cache = {
                template.id: template for template in self.sqltemplates
            }
        return templates_id in self.sqltemplate_cache
