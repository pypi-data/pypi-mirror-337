import datetime
import logging
from typing import Literal

from pydantic import BaseModel, Field

from cloecore.utils import writer

from .execute_pipeline_activity import ExecutePipelineActivity

logger = logging.getLogger(__name__)


class PipelineResourceProperties(BaseModel):
    activities: list[ExecutePipelineActivity]
    parameters: dict[str, str] = {}
    variables: dict[str, str] = {}
    folder: dict[str, str] = {}
    annotations: list[str] = []
    last_publish_time: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase


class PipelineResource(BaseModel):
    name: str
    properties: PipelineResourceProperties
    arm_type: Literal["Microsoft.DataFactory/factories/pipelines"] = Field(
        default="Microsoft.DataFactory/factories/pipelines", alias="type"
    )

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

    def set_name_prefix(self, prefix: str) -> None:
        if isinstance(self.name, str):
            if len(self.name) + len(prefix) > 140:
                logger.error(
                    "Length of pipeline name %s + prefix %s but must not exceed 140.",
                    self.name,
                    prefix,
                )
                raise SystemExit("Prefix too long.")
        self.prefix = prefix
        self.name = f"{self.prefix}{self.name}"
