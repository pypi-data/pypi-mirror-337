import logging
import pathlib

logger = logging.getLogger(__name__)


def read_text_from_disk(full_path: pathlib.Path) -> str:
    """
    Central endpoint for all functions/classes
    to read text files from disk.
    """
    with open(full_path) as file:
        file_content = file.read()
    logger.debug("Read file %s.", full_path)
    return file_content
