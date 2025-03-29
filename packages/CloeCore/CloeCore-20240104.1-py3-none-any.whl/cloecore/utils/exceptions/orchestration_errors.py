import logging

from pydantic import ValidationError

from cloecore.utils import exceptions

from .beautify_errors import beautify_errors

logger = logging.getLogger(__name__)


class BatchstepError:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.base: ValidationError | None = None
        self.dependencies: list[ValidationError] = []

    @property
    def is_charged(self) -> bool:
        if self.base is not None:
            return True
        if len(self.dependencies) > 1:
            return True
        return False

    def report_batchstep_errors(self, tabs: int) -> str:
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
        for c_error in self.dependencies:
            error_message += f"\n{b_indentation}:\n{beautify_errors(c_error, tabs + 2)}"
        error_message += "\n"
        return error_message


class BatchError:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.base: ValidationError | None = None
        self.batchstep_error: list[BatchstepError] = []

    @property
    def is_charged(self) -> bool:
        if self.base is not None:
            return True
        if any([batchstep.is_charged for batchstep in self.batchstep_error]):
            return True
        return False

    def report_batchstep_errors(self, tabs: int) -> str:
        error_message = ""
        r_indent = "\t" * tabs
        for batchstep in self.batchstep_error:
            error_message += batchstep.report_batchstep_errors(tabs + 1)
        if len(error_message) > 1:
            return f"{r_indent}Batchstep Error Report:\n{error_message}"
        else:
            return f"{r_indent}Batchstep Validation: Passed"

    def report_batch_errors(self, tabs: int) -> str:
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
        error_message += self.report_batchstep_errors(tabs)
        return error_message


class OrchestrationError:
    def __init__(self) -> None:
        self.batch_errors: list[BatchError | ValidationError] = []

    @property
    def is_charged(self) -> bool:
        if any(
            [
                batch.is_charged
                for batch in self.batch_errors
                if not isinstance(batch, ValidationError)
            ]
        ):
            return True
        return False

    def report_batch_errors(self, tabs: int) -> str:
        error_message = ""
        r_indent = "\t" * tabs
        for batch in self.batch_errors:
            if not isinstance(batch, ValidationError):
                error_message += batch.report_batch_errors(tabs + 1)
        if len(error_message) > 1:
            return f"{r_indent}Batch Error Report:\n{error_message}"
        else:
            return f"{r_indent}Batch Validation: Passed"

    def _create_report(self) -> str:
        report_message = ""
        report_message += f"\n{self.report_batch_errors(1)}"
        return report_message

    def return_report(self) -> tuple[bool, str]:
        return self.is_charged, self._create_report()

    def log_report(self) -> None:
        report_message = self._create_report()
        logger.info("Orchestration Report:%s", report_message)
        if self.is_charged:
            raise exceptions.ValidationError()
