import pytest
from src.api import JsonPlaceholderApi


@pytest.fixture(scope="session", autouse=True)
def json_placeholder_api():
    base_url = "https://jsonplaceholder.typicode.com"
    yield JsonPlaceholderApi(base_url=base_url)
