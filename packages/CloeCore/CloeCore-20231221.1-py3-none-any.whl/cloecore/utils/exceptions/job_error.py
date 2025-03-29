import logging

from pydantic import ValidationError

from cloecore.utils import exceptions

from .beautify_errors import beautify_errors

logger = logging.getLogger(__name__)


class ExecSQLError:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.base: ValidationError | None = None
        self.queries: dict[str, ValidationError] = {}

    @property
    def is_charged(self) -> bool:
        if self.base is not None:
            return True
        if len(self.queries) > 1:
            return True
        return False

    def report_exec_sql_errors(self, tabs: int) -> str:
        error_message = ""
        indentation = "\t" * tabs
        b_indentation = "\t" * (tabs + 1)
        q_indentation = "\t" * (tabs + 1)
        if self.base is not None:
            error_message += (
                f"{indentation}name: {self.name}\n{b_indentation}"
                f"base:\n{beautify_errors(self.base, tabs + 2)}"
            )
        else:
            error_message += f"{indentation}name: {self.name}\n{b_indentation}"
        for c_name, c_error in self.queries.items():
            error_message += (
                f"\n{q_indentation}{c_name}:\n{beautify_errors(c_error, tabs + 2)}"
            )
        error_message += "\n"
        return error_message


class JobError:
    def __init__(self) -> None:
        self.exec_sql: list[ExecSQLError] = []
        self.db_to_fs: dict[str, ValidationError] = {}
        self.fs_to_db: dict[str, ValidationError] = {}
        self.fs_to_fs: dict[str, ValidationError] = {}

    @property
    def is_charged(self) -> bool:
        for attribute, value in self.__dict__.items():
            if attribute == "exec_sql":
                for table in self.exec_sql:
                    if table.is_charged:
                        return True
            else:
                if len(value) >= 1:
                    return True
        return False

    def report_exec_sql_errors(self, tabs: int) -> str:
        error_message = ""
        r_indent = "\t" * tabs
        for exec_sql in self.exec_sql:
            error_message += exec_sql.report_exec_sql_errors(tabs + 1)
        if len(error_message) > 1:
            return f"{r_indent}Exec SQL Error Report:\n{error_message}"
        else:
            return f"{r_indent}Exec SQL Validation: Passed"

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
            if attribute == "exec_sql":
                report_message += f"\n{self.report_exec_sql_errors(1)}"
            else:
                report_message += f"\n{self.report_errors(attribute, 1, value)}"
        return report_message

    def return_report(self) -> tuple[bool, str]:
        return self.is_charged, self._create_report()

    def log_report(self) -> None:
        report_message = self._create_report()
        logger.info("Job Report:%s", report_message)
        if self.is_charged:
            raise exceptions.ValidationError()
