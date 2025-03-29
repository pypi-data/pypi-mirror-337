import re

REGEX_ALPHANUMERIC_W = r"[^a-zA-ZäöüÄÖÜß0-9_ ]"


def name_alphanumeric_w_replace(name: str) -> str:
    """Function checks for non alphanumeric character
    and removes whitespace

    Args:
        name (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    if re.search(REGEX_ALPHANUMERIC_W, name):
        raise ValueError("must be alphanumeric including '_', ' '")
    return name.replace(" ", "_")


def name_alphanumeric(name: str) -> str:
    """Function checks for non alphanumeric character.

    Args:
        name (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    if re.search(REGEX_ALPHANUMERIC_W, name):
        raise ValueError("must be alphanumeric including '_', ' '")
    return name


def name_alphanumeric_table_name(name: str, values: dict[str, str]) -> str:
    """Function checks for non alphanumeric character. Special
    function for table name checks also taking level into account

    Args:
        name (str): _description_
        values (dict[str, str]): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    if values["level"] in (
        "core",
        "lu",
        "ver",
    ) and re.search(REGEX_ALPHANUMERIC_W, name):
        raise ValueError(
            "must be alphanumeric including '_',"
            " ' ' for all levels except src/stg/derived"
        )
    return name


def name_alphanumeric_table_columns(name: str, values: dict[str, str]) -> str:
    """Function checks for non alphanumeric character. Special
    function for table column name checks also taking level into account

    Args:
        name (str): _description_
        values (dict[str, str]): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """
    if values["table_level"] in (
        "core",
        "lu",
        "ver",
    ) and re.search(REGEX_ALPHANUMERIC_W, name):
        raise ValueError(
            "must be alphanumeric including '_',"
            " ' ' for all levels except src/stg/derived"
        )
    return name
