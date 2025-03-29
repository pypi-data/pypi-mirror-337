import logging
import pathlib

logger = logging.getLogger(__name__)


def read_text_from_disk(full_path: pathlib.Path) -> str:
    """Central endpoint for all functions/classes
    to read text files from disk.

    Args:
        file_path_parts list | str: _description_

    Returns:
        str: _description_
    """
    with open(full_path, "r") as file:
        file_content = file.read()
    logger.debug("Read file %s.", full_path)
    return file_content
