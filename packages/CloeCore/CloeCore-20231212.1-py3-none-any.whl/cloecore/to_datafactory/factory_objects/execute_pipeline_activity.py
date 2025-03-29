from __future__ import annotations

import logging
import uuid
from typing import Literal

from pydantic import BaseModel, Field, validator

from cloecore.utils import writer

logger = logging.getLogger(__name__)


class ActivityUserProperties(BaseModel):
    batch_id: int
    batchstep_id: uuid.UUID
    job_id: uuid.UUID
    job_name: str

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

    def _get_user_properties(self) -> list[dict[str, str]]:
        properties = [
            {"name": "batch_id", "value": str(self.batch_id)},
            {"name": "batchstep_id", "value": str(self.batchstep_id)},
            {"name": "job_id", "value": str(self.job_id)},
            {"name": "job_name", "value": str(self.job_name)},
        ]
        return properties


class ActivityDependency(BaseModel):
    activity: str
    dependency_conditions: list[Literal["Succeeded", "Completed"]]

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase


class ExecutePipelineTypeProperties(BaseModel):
    pipeline: dict[str, str]
    wait_on_completion: bool = True
    parameters: dict[str, str | None] = {}

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase


class ExecutePipelineActivity(BaseModel):
    batchstep_id: uuid.UUID | None = Field(exclude=True)
    name: str
    description = ""
    depends_on: list[ActivityDependency] = []
    pipeline_variables: list[str] = Field(default=[], exclude=True)
    user_properties: list[ActivityUserProperties] = []
    arm_type: Literal["ExecutePipeline"] = Field(
        default="ExecutePipeline", alias="type"
    )
    type_properties: ExecutePipelineTypeProperties

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camelcase

    @validator("name")
    def catalog_name_template(cls, value, values, **kwargs):
        if len(value) > 55:
            logger.warning(
                (
                    "Length of activity name %s is %s but must not exceed 55."
                    " It was shortened."
                ),
                value,
                len(value),
            )
            value = f"{value[0:46]}{str(values['batchstep_id']).split('-')[0]}"
        return value


ActivityDependency.update_forward_refs()
