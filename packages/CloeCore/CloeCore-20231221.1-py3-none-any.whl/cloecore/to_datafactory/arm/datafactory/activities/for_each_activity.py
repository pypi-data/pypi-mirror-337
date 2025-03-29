from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity


class ForEachActivity(BaseActivity):
    def __init__(
        self,
        name: str,
        items: dict,
        is_sequential: bool | None = True,
        activities: list[BaseActivity] | None = None,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(name, description, act_depends_on, res_depends_on)
        self.items = items
        self.is_sequential = is_sequential
        self.activities = activities or []

    def get_item_expression(self, name: str | None = None) -> dict[str, str]:
        if name is not None:
            return {"value": f"@item().{name}", "type": "Expression"}
        return {"value": "@item()", "type": "Expression"}

    def add_activities(self, activity: list[BaseActivity]) -> None:
        self.activities += activity

    def _prepare_activities(self) -> None:
        for act in self.activities:
            act.set_user_properties(
                self.job_name, self.job_id, self.batch_id, self.batchstep_id
            )

    def get_res_deps_of(self) -> list:
        for act in self.activities:
            self.res_depends_on += act.get_res_deps_of()
        return super().get_res_deps_of()

    def _to_arm(self) -> dict:
        self._prepare_activities()
        return {
            "type": "ForEach",
            "typeProperties": {
                "isSequential": self.is_sequential,
                "items": self.items,
                "activities": [act.to_arm() for act in self.activities],
            },
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        base = super().to_arm()
        base |= self._to_arm()
        return base
