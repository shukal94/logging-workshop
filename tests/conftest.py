import pytest
from src.api import JsonPlaceholderApi, HttpClient
from src.utils import load_config


CONFIG_PATH = "config.ini"


@pytest.fixture(scope="session", autouse=True)
def config():
    return load_config(path=CONFIG_PATH)


@pytest.fixture(scope="session", autouse=True)
def http_client(config):
    http_config = config["http"]
    max_retries = http_config.get("max_retries")
    retry_delay = http_config.get("retry_delay")
    return HttpClient(max_retries=max_retries, retry_delay=retry_delay)


@pytest.fixture(scope="session", autouse=True)
def json_placeholder_api(config, http_client):
    api_config = config["api"]
    base_url = api_config.get("base_url")
    yield JsonPlaceholderApi(http_client=http_client, base_url=base_url)
