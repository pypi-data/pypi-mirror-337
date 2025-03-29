import json
import logging
import pathlib
import re

logger = logging.getLogger(__name__)
CAMEL_TO_SNAKE_PATTERN_FIRST = re.compile(r"(.)([A-Z][a-z]+)")
CAMEL_TO_SNAKE_PATTERN_LAST = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(name: str):
    name = re.sub(CAMEL_TO_SNAKE_PATTERN_FIRST, r"\1_\2", name)
    return re.sub(CAMEL_TO_SNAKE_PATTERN_LAST, r"\1_\2", name).lower()


def dict_keys_to_snake(model: dict | list):
    if isinstance(model, list):
        return [
            dict_keys_to_snake(i) if isinstance(i, (dict, list)) else i for i in model
        ]
    return {
        camel_to_snake(a): dict_keys_to_snake(b) if isinstance(b, (dict, list)) else b
        for a, b in model.items()
    }


def read_jsons_from_disk(
    file_paths: list[pathlib.Path], transform_to_snake: bool = False
) -> dict[str, dict]:
    """Central endpoint for all functions/classes
    to read multiple json files from disk.

    Args:
        file_paths (list): _description_

    Returns:
        dict[str, dict | list]: _description_
    """
    all_jsons = {}
    for i in file_paths:
        content = read_json_from_disk(i)
        if transform_to_snake is True:
            trans_content = dict_keys_to_snake(content)
        all_jsons[str(i)] = trans_content
    logger.debug("Read %s files.", len(file_paths))
    return all_jsons


def find_model_object_path(
    file_paths: list[pathlib.Path], model_id: str
) -> pathlib.Path | None:
    for i in file_paths:
        content = read_json_from_disk(i)
        if (
            isinstance(content, dict)
            and "modelID" in content
            and "modelContent" in content
        ):
            if content["modelID"] == model_id:
                return i
    return None


def read_models_from_disk(file_paths: list[pathlib.Path]) -> dict[str, list]:
    """Central endpoint for all functions/classes
    to read multiple json files from disk.

    Args:
        file_paths (list): _description_

    Returns:
        dict[str, dict | list]: _description_
    """
    all_jsons = {}
    for i in file_paths:
        content = read_json_from_disk(i)
        if (
            isinstance(content, dict)
            and "modelID" in content
            and "modelContent" in content
        ):
            trans_content = dict_keys_to_snake(content["modelContent"])
            all_jsons[content["modelID"]] = trans_content
        else:
            logger.info(
                (
                    "Skipping %s file. Not a valid CLOE JSON"
                    "(modelID and/or modelContent missing)"
                ),
                i,
            )
    logger.debug("Read %s files.", len(file_paths))
    return all_jsons


def read_json_from_disk(full_path: pathlib.Path) -> dict:
    """Central endpoint for all functions/classes
    to read a json file from disk.

    Args:
        file_path_parts (list | str): _description_

    Returns:
        dict | list: _description_
    """
    with open(full_path, "r") as json_file:
        json_data = json.load(json_file)
    logger.debug("Read json file in %s.", full_path)
    return json_data
