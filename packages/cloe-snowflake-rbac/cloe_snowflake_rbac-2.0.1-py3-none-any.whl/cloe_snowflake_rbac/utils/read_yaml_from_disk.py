import logging
import os
import pathlib

import yaml

logger = logging.getLogger(__name__)


def read_yaml_from_disk(full_path: pathlib.Path) -> dict | None:
    """
    Reads a YAML file or combines multiple YAML files in a directory into a single dictionary.
    """
    if full_path.is_file():
        # If full_path is a file, load it directly
        with open(full_path) as file:
            file_content = yaml.safe_load(file)
        logger.info("Read YAML from %s.", full_path)
        return file_content
    elif full_path.is_dir():
        # If full_path is a directory, combine YAML files in the directory
        combined_content = {}
        for file_name in os.listdir(full_path):
            if file_name.endswith(".yaml") or file_name.endswith(".yml"):
                file_path = full_path / file_name
                with open(file_path) as file:
                    file_content = yaml.safe_load(file)
                combined_content.update(file_content)
        if combined_content:
            logger.info("Combined YAML files in directory %s.", full_path)
            return combined_content
    # If neither a file nor a directory, return None
    return None
