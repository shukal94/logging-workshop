import logging
import os
import src.utils as utils
from datetime import datetime
from tests.conftest import DOWNLOADS_PATH, USER_TEMPLATE_PATH, TEST_FILES_PATH

REMOTE_ROOT_PATH = "/"
REMOTE_EXAMPLES_PATH = "/expamples"
FILENAME = "readme.txt"

LOGGER = logging.getLogger("test") # logger object is a singleton, we can use one of the loggers defined in logging.ini
SAMPLE_NAME = "John"
SAMPLE_OCCUPATION = "SDET 4"
SAMPLE_ADDRESS = "74 Kostavas Tbilisi 01-411, Georgia"


def test_ls(sftp_client):
    LOGGER.info("Validating root directory is not empty.")
    ls_result = sftp_client.ls(remote_path=REMOTE_ROOT_PATH)
    assert len(ls_result) != 0, "Nothing in root."


def test_get(sftp_client):
    LOGGER.info("Validating file download.")
    path_to_download = f"{DOWNLOADS_PATH}/{FILENAME}"
    sftp_client.get(
        remote_path=f"{REMOTE_ROOT_PATH}/{FILENAME}",
        local_path= path_to_download
    )
    assert os.path.exists(path_to_download), "Download failed."


def test_put(sftp_client):
    LOGGER.info(f"Generating a new user from template {USER_TEMPLATE_PATH}.")
    content = utils.read_from_file(USER_TEMPLATE_PATH)
    content = content.format(name=SAMPLE_NAME, occupation=SAMPLE_OCCUPATION, address=SAMPLE_ADDRESS)

    filename = f"user_{datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')}.txt"
    path_to_save = f"{TEST_FILES_PATH}/{filename}"
    LOGGER.info(f"Saving a new user data into {path_to_save}.")
    utils.write_to_file(content, path_to_save)

    LOGGER.info("Uploading file and validating success upload.")
    sftp_client.put(local_path=path_to_save, remote_path=REMOTE_EXAMPLES_PATH)
    assert filename in sftp_client.ls(REMOTE_EXAMPLES_PATH), f"File {filename} was not uploaded."
