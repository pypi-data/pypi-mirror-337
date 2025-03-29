from __future__ import annotations

import json
import logging
import pathlib
from typing import ClassVar, Type

from pydantic import BaseModel, Field, ValidationError, validator

import cloecore.utils.writer as writer
from cloecore.utils.model import validators
from cloecore.utils.model.modeler.powerpipe import PowerPipe
from cloecore.utils.model.modeler.simple_pipe import SimplePipe

logger = logging.getLogger(__name__)


class Pipes(BaseModel):
    """Base class for loading CLOE Pipe model objects."""

    subfolder_path: ClassVar[pathlib.Path] = pathlib.Path("pipes")

    pipes: list[SimplePipe | PowerPipe] = Field(default=[], exclude=True)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = writer.to_lower_camel_case

    @validator("pipes")
    def child_uniqueness_check(cls, value: list[SimplePipe | PowerPipe]):
        validators.find_non_unique(value, "name")
        return value

    @classmethod
    def read_instances_from_disk(
        cls, input_path: pathlib.Path
    ) -> tuple[Pipes, list[ValidationError | json.JSONDecodeError]]:
        instances: list[SimplePipe | PowerPipe] = []
        errors = []
        if not input_path.exists():
            raise FileNotFoundError(f"Directory not found: {input_path}")

        instances_path = input_path / cls.subfolder_path
        sub_pipes: list[Type[SimplePipe] | Type[PowerPipe]] = [
            SimplePipe,
            PowerPipe,
        ]
        for sub_pipe in sub_pipes:
            sub_instances, sub_errors = sub_pipe.read_instances_from_disk(
                instances_path / sub_pipe.__name__.lower()
            )
            instances += sub_instances
            errors += sub_errors
        try:
            instance = cls(pipes=instances)
        except ValidationError as e:
            errors.append(e)

        return instance, errors

    def write_to_disk(self, output_path: pathlib.Path) -> None:
        for child in self.pipes:
            child.write_to_disk(
                output_path / self.subfolder_path / child.__class__.__name__.lower()
            )

    def get_pipes_of_type(
        self,
        pipe_type: Type[SimplePipe] | Type[PowerPipe],
    ) -> list[SimplePipe | PowerPipe]:
        """
        Filters the pipes list based on the given pipe type.

        :param pipe_type: Type of the pipe
        :return: List of pipes of the specified type
        """
        return [pipe for pipe in self.pipes if isinstance(pipe, pipe_type)]
