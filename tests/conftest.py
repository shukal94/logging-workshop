import os
import pytest
import json
import src.utils as utils
from playwright.sync_api import sync_playwright
from src.api import JsonPlaceholderApi, HttpClient
from src.db import SqliteClient, TestDbClient
from src.ssh import SshClient


CONFIG_PATH = "config.ini"
DOWNLOADS_PATH = ".testdata/downloads"
DB_SCRIPT_PATH = "init_db.sql"


@pytest.fixture(scope="session", autouse=True)
def mkdirs():
    os.makedirs(f"{os.getcwd()}/{DOWNLOADS_PATH}", exist_ok=True)


@pytest.fixture(scope="session")
def config():
    return utils.load_config(path=CONFIG_PATH)


@pytest.fixture(scope="session")
def http_client(config):
    http_config = config["http"]
    max_retries = http_config.get("max_retries")
    retry_delay = http_config.get("retry_delay")
    return HttpClient(max_retries=max_retries, retry_delay=retry_delay)


@pytest.fixture(scope="session")
def json_placeholder_api(config, http_client):
    api_config = config["api"]
    base_url = api_config.get("base_url")
    yield JsonPlaceholderApi(http_client=http_client, base_url=base_url)


@pytest.fixture(scope="session")
def sftp_client(config):
    sftp_config = config["sftp"]
    host = sftp_config.get("host")
    port = sftp_config.getint("port")
    username = sftp_config.get("username")
    password = utils.env("SFTP_PWD", safe=False)

    ssh_client = SshClient(host, port, username, password)
    ssh_client.connect_ssh()
    ssh_client.connect_sftp()

    yield ssh_client

    ssh_client.close()


@pytest.fixture(scope="session")
def test_db_client(config):
    db_config = config["db"]
    dialect = db_config.get("dialect")
    schema = db_config.get("schema")
    sql_client = None
    if dialect == 'sqlite3':
        sql_client = SqliteClient(schema=schema)
        sql_client.connect()
        sql_client.get_cursor()
    db_client = TestDbClient(schema=schema, db_client=sql_client)
    db_client.initialize(script_path=DB_SCRIPT_PATH)

    yield db_client

    sql_client.close()


@pytest.fixture(scope="function")
def pw():
    with sync_playwright() as playwright_instance:
        yield playwright_instance


@pytest.fixture(scope="function")
def browser(config, pw):
    ui_config = config["ui"]
    headless = ui_config.getboolean("headless")
    timeout = ui_config.getint("timeout")
    browser = pw.chromium.launch(headless=headless, timeout=timeout)

    yield browser

    browser.close()


@pytest.fixture(scope="function")
def browser_context(config, browser):
    ui_config = config["ui"]
    base_url = ui_config.get("base_url")
    viewport = json.loads(ui_config.get("viewport"))
    ctx = browser.new_context(viewport=viewport, base_url=base_url)

    yield ctx

    ctx.close()


@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()

    yield page

    page.close()
