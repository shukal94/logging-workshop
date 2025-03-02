import os

REMOTE_ROOT_PATH = "/"
LOCAL_DOWNLOADS_PATH = ".testdata/downloads"
FILENAME = "readme.txt"


def test_ls(sftp_client):
    ls_result = sftp_client.ls(remote_path=REMOTE_ROOT_PATH)
    assert len(ls_result) != 0, "Nothing in root."


def test_get(sftp_client):
    path_to_download = f"{LOCAL_DOWNLOADS_PATH}/{FILENAME}"
    sftp_client.get(
        remote_path=f"{REMOTE_ROOT_PATH}/{FILENAME}",
        local_path= path_to_download
    )
    assert os.path.exists(path_to_download), "Download failed."
