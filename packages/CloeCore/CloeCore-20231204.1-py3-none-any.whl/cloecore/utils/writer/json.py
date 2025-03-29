import json
import logging
import pathlib
import re

logger = logging.getLogger(__name__)


def to_lower_camelcase(name: str) -> str:
    name = "".join(word.capitalize() for word in name.split("_"))
    name = f"{name[:1].lower()}{name[1:]}"
    name = re.sub(r"Id$", "ID", name)
    return name


def write_dict_to_disk_json(json_object: dict, full_path: pathlib.Path) -> None:
    """Central endpoint function for all
    objects to write a json to disk.

    Args:
        json_object (dict): _description_
        file_path (str): _description_
        file_name (str): _description_
    """
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w") as file:
        json.dump(json_object, file, indent=4)
    logger.debug("Wrote dict to %s.", full_path)
