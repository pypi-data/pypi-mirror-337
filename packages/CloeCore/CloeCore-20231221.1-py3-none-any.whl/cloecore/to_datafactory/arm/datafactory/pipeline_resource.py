from __future__ import annotations

import logging

from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity
from cloecore.to_datafactory.arm.general import parameter
from cloecore.to_datafactory.arm.general.base import ARMBase

logger = logging.getLogger(__name__)


class PipelineResource(ARMBase):
    type_short: str = "pipelines"
    type_fullpath: str = "Microsoft.DataFactory/factories/pipelines"
    reference_type_name: str = "PipelineReference"

    def __init__(
        self,
        name: str,
        pipe_activities: list[BaseActivity],
        required_arm_variables: dict[str, str] | None = None,
        folder_name: str | None = None,
    ) -> None:
        deps = [
            (
                "[resourceId('Microsoft.DataFactory/factories',"
                f" {parameter.Parameter('factoryName').get_expression()})]"
            )
        ]
        self.activities = pipe_activities
        super().__init__(
            name=name,
            required_arm_variables=required_arm_variables,
            depends_on=deps,
            required_arm_parameters=parameter.Parameter("factoryName").get_reference(),
        )
        self.folder_name = folder_name
        self.prefix: str = ""

    def deduplicate_activity_names(self) -> None:
        activity_names: dict[str, int] = {}
        for activity in self.activities:
            if activity.name in activity_names:
                activity_names[activity.name] += 1
                activity.name = (
                    f"{activity.name[:(55-len(str(activity_names[activity.name])))]}"
                    f" {activity_names[activity.name]}"
                )
            else:
                activity_names[activity.name] = 1

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

    def _get_activity_dependencies(self) -> list[str]:
        act_deps: list[str] = []
        for act in self.activities:
            act_deps += act.get_res_deps_of()
        return act_deps

    def _get_activity_variables(self) -> dict[str, dict]:
        act_vars = {}
        for act in self.activities:
            for var in act.pipeline_variables:
                if var not in act_vars:
                    act_vars[var] = {"type": "string"}
        return act_vars

    def _get_activity_parameters(self) -> dict[str, dict]:
        act_params = {}
        for act in self.activities:
            for param in act.pipeline_parameters:
                if param not in act_params:
                    act_params[param] = {"type": "string"}
        return act_params

    def to_arm(self) -> dict[str, dict | str | list]:
        self.deduplicate_activity_names()
        self.depends_on += self._get_activity_dependencies()
        self.properties = {
            "activities": [act.to_arm() for act in self.activities],
            "parameters": self._get_activity_parameters(),
            "annotations": [],
            "folder": {"name": self.folder_name},
        }
        self.properties["variables"] = self._get_activity_variables()
        return super().to_arm()
