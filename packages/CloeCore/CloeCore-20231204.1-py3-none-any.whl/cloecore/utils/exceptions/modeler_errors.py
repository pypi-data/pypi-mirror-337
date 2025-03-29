import logging

from pydantic import ValidationError

from cloecore.utils import exceptions

from .beautify_errors import beautify_errors

logger = logging.getLogger(__name__)


class PowerPipeLookupError:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.base: ValidationError | None = None
        self.return_column_mapping: dict[str, ValidationError] = {}
        self.parameter_mapping: list[ValidationError] = []

    @property
    def is_charged(self) -> bool:
        if self.base is not None:
            return True
        if len(self.return_column_mapping) > 1:
            return True
        if len(self.parameter_mapping) > 1:
            return True
        return False

    def report_pp_lu_errors(self, tabs: int) -> str:
        error_message = ""
        indentation = "\t" * tabs
        b_indentation = "\t" * (tabs + 1)
        if self.base is not None:
            error_message += (
                f"{indentation}name: {self.name}\n{b_indentation}"
                f"base:\n{beautify_errors(self.base, tabs + 2)}"
            )
        else:
            error_message += f"{indentation}name: {self.name}\n{b_indentation}"
        for c_name, c_error in self.return_column_mapping.items():
            error_message += (
                f"\n{b_indentation}{c_name}:\n{beautify_errors(c_error, tabs + 2)}"
            )
        for c_error in self.parameter_mapping:
            error_message += f"\n{b_indentation}\n{beautify_errors(c_error, tabs + 2)}"
        error_message += "\n"
        return error_message


class PowerPipeError:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.base: ValidationError | None = None
        self.column_mapping: dict[str, ValidationError] = {}
        self.source_tables: dict[str, ValidationError] = {}
        self.lookups: list[PowerPipeLookupError] = []

    @property
    def is_charged(self) -> bool:
        if self.base is not None:
            return True
        if len(self.column_mapping) > 1:
            return True
        if len(self.source_tables) > 1:
            return True
        if any([lookup.is_charged for lookup in self.lookups]):
            return True
        return False

    def report_lu_errors(self, tabs: int) -> str:
        error_message = ""
        r_indent = "\t" * tabs
        for lookup in self.lookups:
            error_message += lookup.report_pp_lu_errors(tabs + 1)
        if len(error_message) > 1:
            return f"{r_indent}DataFlow Lookup Error Report:\n{error_message}"
        else:
            return f"{r_indent}DataFlow Lookup Validation: Passed"

    def report_pp_errors(self, tabs: int) -> str:
        error_message = ""
        indentation = "\t" * tabs
        b_indentation = "\t" * (tabs + 1)
        if self.base is not None:
            error_message += (
                f"{indentation}name: {self.name}\n{b_indentation}"
                f"base:\n{beautify_errors(self.base, tabs + 2)}"
            )
        else:
            error_message += f"{indentation}name: {self.name}\n{b_indentation}"
        for attribute in [self.column_mapping, self.source_tables]:
            for c_name, c_error in attribute.items():
                error_message += (
                    f"\n{b_indentation}{c_name}:\n{beautify_errors(c_error, tabs + 2)}"
                )
        error_message += "\n"
        return error_message


class SimplePipeError:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.base: ValidationError | None = None
        self.table_mapping: dict[str, ValidationError] = {}

    @property
    def is_charged(self) -> bool:
        if self.base is not None:
            return True
        if len(self.table_mapping) > 1:
            return True
        return False

    def report_sp_errors(self, tabs: int) -> str:
        error_message = ""
        indentation = "\t" * tabs
        b_indentation = "\t" * (tabs + 1)
        if self.base is not None:
            error_message += (
                f"{indentation}name: {self.name}\n{b_indentation}"
                f"base:\n{beautify_errors(self.base, tabs + 2)}"
            )
        else:
            error_message += f"{indentation}name: {self.name}\n{b_indentation}"
        for c_name, c_error in self.table_mapping.items():
            error_message += (
                f"\n{b_indentation}{c_name}:\n{beautify_errors(c_error, tabs + 2)}"
            )
        error_message += "\n"
        return error_message


class ModelerError:
    def __init__(self) -> None:
        self.power_pipe_error: list[PowerPipeError] = []
        self.simple_pipe_error: list[SimplePipeError] = []

    @property
    def is_charged(self) -> bool:
        for attribute, value in self.__dict__.items():
            if attribute == "power_pipe_error":
                if any([pipe.is_charged for pipe in self.power_pipe_error]):
                    return True
            elif attribute == "simple_pipe_error":
                if any([pipe.is_charged for pipe in self.simple_pipe_error]):
                    return True
            else:
                if len(value) >= 1:
                    return True
        return False

    def report_pp_errors(self, tabs: int) -> str:
        error_message = ""
        r_indent = "\t" * tabs
        for pipe in self.power_pipe_error:
            error_message += pipe.report_pp_errors(tabs + 1)
        if len(error_message) > 1:
            return f"{r_indent}DataFlow Error Report:\n{error_message}"
        else:
            return f"{r_indent}DataFlow Validation: Passed"

    def report_sp_errors(self, tabs: int) -> str:
        error_message = ""
        r_indent = "\t" * tabs
        for pipe in self.simple_pipe_error:
            error_message += pipe.report_sp_errors(tabs + 1)
        if len(error_message) > 1:
            return f"{r_indent}CustomDataFlow Error Report:\n{error_message}"
        else:
            return f"{r_indent}CustomDataFlow Validation: Passed"

    @staticmethod
    def report_errors(
        report_name: str, tabs: int, errors: dict[str, ValidationError]
    ) -> str:
        error_message = ""
        r_indent = "\t" * tabs
        e_indent = "\t" * (tabs + 1)
        for name, v_error in errors.items():
            error_message += f"{e_indent}{name}:\n{beautify_errors(v_error, tabs + 2)}"
        if len(error_message) > 1:
            return f"{r_indent}{report_name} Error Report:\n{error_message}"
        else:
            return f"{r_indent}{report_name} Validation: Passed"

    def _create_report(self) -> str:
        report_message = ""
        for attribute, value in self.__dict__.items():
            if attribute == "power_pipe_error":
                report_message += f"\n{self.report_pp_errors(1)}"
            else:
                report_message += f"\n{self.report_sp_errors(1)}"
        return report_message

    def return_report(self) -> tuple[bool, str]:
        return self.is_charged, self._create_report()

    def log_report(self) -> None:
        report_message = self._create_report()
        logger.info("Modeler Report:%s", report_message)
        if self.is_charged:
            raise exceptions.ValidationError()
