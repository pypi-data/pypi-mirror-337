from datetime import datetime, timedelta

from croniter import croniter

from cloecore.to_datafactory.arm.datafactory.pipeline_resource import PipelineResource
from cloecore.to_datafactory.arm.general import parameter
from cloecore.to_datafactory.arm.general.base import ARMBase


class Trigger(ARMBase):
    type_short: str = "triggers"
    type_fullpath: str = "Microsoft.DataFactory/factories/triggers"
    reference_type_name: str = "PipelineReference"

    def __init__(
        self,
        pipeline: PipelineResource,
        cron: str,
        timezone: str,
        required_arm_variables: dict[str, str] | None = None,
    ) -> None:
        deps = [
            (
                "[resourceId('Microsoft.DataFactory/factories',"
                f" {parameter.Parameter('factoryName').get_expression()})]"
            )
        ]
        super().__init__(
            name=f"Trigger_{pipeline.name}",
            depends_on=deps + pipeline.get_dependency_on(),
            required_arm_parameters=parameter.Parameter("factoryName").get_reference(),
            required_arm_variables=required_arm_variables,
        )
        self.pipeline = pipeline
        self.cron = cron
        self.timezone = timezone
        self.schedule = None

    def _get_type_properties(self) -> dict:
        d_tomorrow = datetime.today() + timedelta(days=1)
        iter = croniter(self.cron, d_tomorrow)
        next_date = iter.get_next(datetime)
        self.starttime = next_date.strftime("%Y-%m-%dT%H:%M:%S")
        base = datetime(2020, 1, 1, 0, 0)
        iter = croniter(self.cron, base)
        next_date = iter.get_next(datetime)
        minutes = []
        hours = []
        weekdays = []
        while (next_date - base) < timedelta(days=31):
            hours.append(next_date.hour)
            minutes.append(next_date.minute)
            weekdays.append(next_date.strftime("%A"))
            next_date = iter.get_next(datetime)
        minutes = list(set(minutes))
        hours = list(set(hours))
        weekdays = list(set(weekdays))
        if len(minutes) != 60 or len(hours) != 24:
            schedule = {"hours": hours, "weekDays": weekdays, "minutes": minutes}
        elif len(weekdays) != 7:
            schedule = {"weekDays": weekdays}
        else:
            schedule = None
        if schedule:
            return {
                "frequency": "Week",
                "interval": 1,
                "startTime": self.starttime,
                "timeZone": self.timezone,
                "schedule": schedule,
            }
        return {
            "frequency": "Week",
            "interval": 1,
            "startTime": self.starttime,
            "timeZone": self.timezone,
        }

    def _get_schedule(self) -> dict:
        return {
            "type": "ScheduleTrigger",
            "runtimeState": "Stopped",
            "annotations": [],
            "typeProperties": {"recurrence": self._get_type_properties()},
            "pipelines": [{"pipelineReference": self.pipeline.get_reference()}],
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        self.properties = self._get_schedule()
        return super().to_arm()
