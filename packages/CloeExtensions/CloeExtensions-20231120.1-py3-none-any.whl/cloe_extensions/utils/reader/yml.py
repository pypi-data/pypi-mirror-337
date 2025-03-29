import logging
import pathlib

import yaml

logger = logging.getLogger(__name__)


def read_yaml_from_disk(full_path: pathlib.Path) -> dict | None:
    """Central endpoint for all functions/classes
    to read a yaml file from disk.

    Args:
        file_path_parts list | str: _description_

    Returns:
        dict: _description_
    """
    with open(full_path, "r") as file:
        file_content = yaml.safe_load(file)
    logger.info("Read file %s.", full_path)
    return file_content
