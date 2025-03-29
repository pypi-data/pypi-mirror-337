import cloecore.to_datafactory.arm.datafactory.datasets.base as dbase
from cloecore.to_datafactory.arm.datafactory.activities import support
from cloecore.to_datafactory.arm.datafactory.activities.base import BaseActivity


class LookupActivity(BaseActivity):
    """LookupActivity wraps BaseActivity."""

    def __init__(
        self,
        name: str,
        source_ds: dbase.DatasetResource,
        source_properties: support.SqlSource,
        ds_params: dict | None = None,
        first_row_only: bool | None = True,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        super().__init__(name, description, act_depends_on, res_depends_on)
        self.source_properties = source_properties
        self.source_ds = source_ds
        self.first_row_only = first_row_only
        self.ds_params = ds_params

    def _to_arm(self) -> dict:
        ds_ref = self.source_ds.get_reference()
        if self.ds_params:
            ds_ref = self.source_ds.get_reference(self.ds_params)
        return {
            "type": "Lookup",
            "policy": {
                "timeout": "0.08:00:00",
                "retry": 0,
                "retryIntervalInSeconds": 30,
                "secureOutput": False,
                "secureInput": False,
            },
            "typeProperties": {
                "source": self.source_properties.to_arm(),
                "dataset": ds_ref,
                "firstRowOnly": self.first_row_only,
            },
        }

    def to_arm(self) -> dict[str, dict | str | list]:
        base = super().to_arm()
        base |= self._to_arm()
        return base
