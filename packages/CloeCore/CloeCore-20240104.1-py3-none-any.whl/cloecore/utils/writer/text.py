import logging
import pathlib

logger = logging.getLogger(__name__)


def write_string_to_disk(string: str, full_path: pathlib.Path) -> None:
    """Central endpoint function for all
    objects to write a string to disk.

    Args:
        string (str): _description_
        file_path (str): _description_
        file_name (str): _description_
    """
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(string)
    logger.debug("Wrote string to %s.", full_path)
