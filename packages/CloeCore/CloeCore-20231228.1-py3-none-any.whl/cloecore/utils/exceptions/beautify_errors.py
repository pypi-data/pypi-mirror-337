from pydantic import ValidationError


def beautify_errors(pydantic_error: ValidationError, tabs: int) -> str:
    error_message = ""
    indentation = "\t" * tabs
    for error in pydantic_error.errors():
        error_message += (
            f"{indentation}{error['loc'][0] : <20} -> {error['msg'] : >20}\n"
        )
    return error_message
