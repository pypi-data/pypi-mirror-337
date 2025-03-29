import logging
import pathlib

logger = logging.getLogger(__name__)


def find_files(folder_path: pathlib.Path) -> list[pathlib.Path]:
    files = [p for p in folder_path.rglob("*.json")]
    logger.debug("The following files in %s were found: +++ %s", folder_path, files)
    return files
