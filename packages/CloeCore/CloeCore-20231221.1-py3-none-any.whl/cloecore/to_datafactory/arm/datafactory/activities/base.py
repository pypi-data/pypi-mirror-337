from __future__ import annotations

import logging
import uuid

logger = logging.getLogger(__name__)


class BaseActivity:
    """Base Activity for all pipeline activites"""

    def __init__(
        self,
        name: str,
        description: str | None = None,
        act_depends_on: list[dict] | None = None,
        res_depends_on: list[str] | None = None,
    ) -> None:
        self.name = name
        self.description = description or ""
        self.act_depends_on: list | list[dict] = act_depends_on or []
        self.res_depends_on: list | list[str] = res_depends_on or []
        self.pipeline_variables: list[str] = []
        self.pipeline_parameters: list[str] = []
        self.batch_id: int = 0
        self.batchstep_id: uuid.UUID = uuid.UUID(int=0)
        self.job_id: uuid.UUID = uuid.UUID(int=0)
        self.required_arm_parameters: dict[str, str] = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if len(name) > 55:
            logger.warning(
                (
                    "Length of activity name %s is %s but must not exceed 55."
                    " It was shortened."
                ),
                name,
                len(name),
            )
            name = name[0:56]
        self._name = name

    def add_activity_dependency(self, activity: BaseActivity, condition: str) -> None:
        self.act_depends_on += [
            {"activity": activity, "dependencyConditions": [condition]}
        ]

    def set_user_properties(
        self,
        job_name: str,
        job_id: uuid.UUID | None = None,
        batch_id: int | None = None,
        batchstep_id: uuid.UUID | None = None,
    ) -> None:
        self.batch_id = batch_id or self.batch_id
        self.batchstep_id = batchstep_id or self.batchstep_id
        self.job_id = job_id or self.job_id
        self.job_name = job_name

    def _get_user_properties(self) -> list[dict[str, str]]:
        properties = [
            {"name": "batch_id", "value": str(self.batch_id)},
            {"name": "batchstep_id", "value": str(self.batchstep_id)},
            {"name": "job_id", "value": str(self.job_id)},
            {"name": "job_name", "value": str(self.job_name)},
        ]
        return properties

    def get_res_deps_of(self) -> list | list[str]:
        return self.res_depends_on

    def _get_pipeline_parameter_expression(self, name: str) -> dict[str, str]:
        self.pipeline_parameters.append(name)
        return {"value": f"@pipeline().parameters.{name}", "type": "Expression"}

    def _get_variable_expression(self, name: str) -> dict[str, str]:
        self.pipeline_variables.append(name)
        return {"value": f"@variables('{name}')", "type": "Expression"}

    @staticmethod
    def _split_expression(input_expression: str, delimiter: str | None = ",") -> str:
        """Returns the input expression wrapped in a ADF split expression.

        Args:
            input_expression (str): _description_
            delimiter (str | None, optional): _description_. Defaults to ",".

        Returns:
            str: _description_
        """
        return f"split({input_expression}, '{delimiter}')"

    @staticmethod
    def _convert_to_string_expression(input_expression: str) -> str:
        return f"string({input_expression})"

    @staticmethod
    def _length_expression(input_expression: str) -> str:
        return f"length({input_expression})"

    @staticmethod
    def _concat_expression(input_expressions: list) -> str:
        input_params = []
        for expression in input_expressions:
            if expression["type"] == "s":
                input_params.append("'" + expression["value"].replace("'", "''") + "'")
            else:
                input_params.append(expression["value"])
        string_params = ",".join(input_params)
        return f"concat({string_params})"

    @staticmethod
    def _less_or_equals_expression(input_expression: str, value: int = 0) -> str:
        return f"lessOrEquals({input_expression}, {value})"

    @staticmethod
    def _if_expression(input_expression: str, true_value: str, false_value: str) -> str:
        return f"if({input_expression}, {true_value}, {false_value})"

    @staticmethod
    def _replace_string_expression(
        input_expression: str, pattern: str, replacement: str
    ) -> str:
        return f"replace({input_expression}, {pattern}, {replacement})"

    def _activity_output(self, output_selector: str | None = None) -> str:
        """Returns and expression to get the output of this activity.

        Args:
            output_selector (str | None, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        outputs_selector = ""
        if output_selector is not None:
            outputs_selector += f".{output_selector}"
        return f"activity('{self.name}').output{outputs_selector}"

    def _lookup_first_row_output(self, column_index: str) -> str:
        return self._activity_output(f"firstRow['{column_index}']")

    def _script_activity_resultset_return_expression(
        self,
        resultsets_index: int | None = None,
        all_rows: bool | None = False,
        rows_index: int | None = None,
        row_selector: str | None = None,
    ) -> str:
        """Returns an expression to get the results from this script activity.

        Args:
            resultsets_index (int | None, optional): _description_. Defaults to None.
            rows_index (int | None, optional): _description_. Defaults to None.
            row_selector (str | None, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        resultsets_selector = "resultSets"
        rows_selector = ""
        if resultsets_index is not None:
            resultsets_selector += f"[{resultsets_index}]"
        if rows_index is not None:
            rows_selector += f".rows[{rows_index}]"
        if resultsets_index is not None and all_rows is True:
            rows_selector += ".rows"
        if rows_index is not None and row_selector is not None:
            rows_selector += f".{row_selector}"
        return self._activity_output(
            output_selector=f"{resultsets_selector}{rows_selector}"
        )

    def get_lookup_first_row_first_col(self, column_index_name: str) -> dict[str, str]:
        """Gets output of a Lookup activity with first row
        set to true. Only selects the output of the first column.

        Returns:
            dict: _description_
        """
        expression = self._convert_to_string_expression(
            self._lookup_first_row_output(column_index=column_index_name)
        )
        return {
            "value": f"@{expression}",
            "type": "Expression",
        }

    def get_activity_output_parameter_array_expression(
        self, array_path: str = "value"
    ) -> dict[str, str]:
        """Returns a standalone expression that selects part of the output of this
        activity based on the set array path.

        Args:
            array_path (str | None, optional): _description_. Defaults to "value".

        Returns:
            dict: _description_
        """
        return {
            "value": f"@{self._activity_output(output_selector=array_path)}",
            "type": "Expression",
        }

    def get_script_activity_all_rows_return_expression(self) -> dict[str, str]:
        """Returns a standalone expression that selects all rows of the output of this
        script activity.

        Returns:
            dict: _description_
        """
        expression = self._script_activity_resultset_return_expression(
            resultsets_index=0, all_rows=True
        )
        return {
            "value": f"@{expression}",
            "type": "Expression",
        }

    def get_script_activity_snowflake_sp_return_expression(
        self, procedure_name: str
    ) -> dict[str, str]:
        """Returns a standalone expression that selects the stored procedure output of
        the first row of the output of this script activity.

        Args:
            procedure_name (str): _description_

        Returns:
            dict: _description_
        """
        script_return_exp = self._script_activity_resultset_return_expression(
            resultsets_index=0, rows_index=0, row_selector=procedure_name
        )
        return {
            "value": f"@{self._split_expression(script_return_exp)}",
            "type": "Expression",
        }

    def _get_activity_dependencies(self) -> list[dict]:
        for dep in self.act_depends_on:
            dep["activity"] = dep["activity"].name
        return self.act_depends_on

    def to_arm(self) -> dict[str, dict | str | list]:
        return {
            "name": self.name,
            "description": self.description,
            "dependsOn": self._get_activity_dependencies(),
            "userProperties": self._get_user_properties(),
        }
