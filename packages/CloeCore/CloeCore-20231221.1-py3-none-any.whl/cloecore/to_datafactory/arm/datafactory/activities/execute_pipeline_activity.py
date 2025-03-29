import uuid

from cloecore.to_datafactory.arm.datafactory import pipeline_resource
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity


class ExecutePipelineActivity(BaseActivity):
    def __init__(
        self,
        name: str,
        pipeline: pipeline_resource.PipelineResource,
        wait_on_completion: bool = True,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(name, description, act_depends_on, res_depends_on)
        self.pipeline = pipeline
        self.exec_pipeline_parameters: dict[str, str | dict[str, str]] = {}
        self.wait_on_completion = wait_on_completion
        self.batch_id = -1
        self.batchstep_id = uuid.UUID(int=0)
        self.job_id = uuid.UUID(int=0)
        self.job_name = "No job connected"

    def _create_parameter(self, name: str, value: str | dict[str, str]) -> None:
        self.exec_pipeline_parameters[name] = value

    def get_res_deps_of(self) -> list:
        self.res_depends_on += self.pipeline.get_dependency_on()
        return super().get_res_deps_of()

    def _to_arm(self) -> dict:
        return {
            "type": "ExecutePipeline",
            "typeProperties": {
                "pipeline": self.pipeline.get_reference(),
                "waitOnCompletion": self.wait_on_completion,
                "parameters": self.exec_pipeline_parameters,
            },
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        base = super().to_arm()
        base |= self._to_arm()
        return base
