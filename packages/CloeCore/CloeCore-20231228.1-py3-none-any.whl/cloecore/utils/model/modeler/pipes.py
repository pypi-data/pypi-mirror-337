import logging
from typing import Type

from pydantic import BaseModel, Field, validator

from cloecore.utils.model import validators
from cloecore.utils.model.modeler.powerpipe import PowerPipe
from cloecore.utils.model.modeler.simple_pipe import SimplePipe

logger = logging.getLogger(__name__)


class Pipes(BaseModel):
    """Base class for loading CLOE Pipe model objects."""

    pipes: list[SimplePipe | PowerPipe] = Field(default=[], exclude=True)

    @validator("pipes")
    def child_uniqueness_check(cls, value: list[SimplePipe | PowerPipe]):
        validators.find_non_unique(value, "name")
        return value

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
