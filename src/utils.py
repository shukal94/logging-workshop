import os
import logging
import configparser

# let's supress utils logger, we always can change level to DEBUG in config
LOGGER = logging.getLogger("utils")


def load_config(path: str):
    LOGGER.debug(f"Reading global project config from {path}")
    config = configparser.ConfigParser()
    config.read(path)
    return config


def env(key: str, safe=True):
    value = os.getenv(key)
    if not safe and not value:
        raise KeyError(f"{key} was not found!")
    return value


def read_from_file(path: str):
    LOGGER.debug(f"Reading from {path}.")
    with open(path, 'r') as file:
        content = file.read()
    return content


def write_to_file(content: str, path: str):
    LOGGER.debug(f"Writing to {path}.")
    with open(path, 'w') as file:
        file.write(content)
