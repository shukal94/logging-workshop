import os
import configparser


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def env(key: str, safe=True):
    value = os.getenv(key)
    if not safe and not value:
        raise KeyError(f"{key} was not found!")
    return value


def read_from_file(path: str):
    with open(path, 'r') as file:
        content = file.read()
    return content
