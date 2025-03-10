import logging

import paramiko

LOGGER = logging.getLogger("sftp")
LOGGER.setLevel(logging.INFO)


class LoggingSftpClient(paramiko.SFTPClient):
    """
    One of the possible approaches: decorator around SFTPClient.
    Instantiation and signatures the same as for original. Uses just once.
    """

    def get(self, remotepath, localpath, callback=None, prefetch=True, max_concurrent_prefetch_requests=None):
        LOGGER.info(f"Downloading {remotepath} to {localpath}")
        return super().get(remotepath, localpath, callback)

    def listdir(self, path: str = '.'):
        LOGGER.info(f"Listing directory {path}")
        ls_result = super().listdir(path)
        LOGGER.info(f"Result: {ls_result}")
        return ls_result

    def put(self, localpath, remotepath, callback=None, confirm=True):
        LOGGER.info(f"Uploading {localpath} to {remotepath}")
        return super().put(localpath, remotepath, callback=None, confirm=True)


class SshClient:
    host: str
    port: int
    username: str
    password: str
    ssh: paramiko.SSHClient
    sftp: LoggingSftpClient # just define it here

    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None
        self.sftp = None

    def connect_ssh(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            allow_agent=False, # to skip key auth
            look_for_keys=False # to skip key auth
        )

    def connect_sftp(self):
        if self.ssh:
            transport = self.ssh.get_transport() # as we cannot instantiate SFTPClient directly
            self.sftp = LoggingSftpClient.from_transport(transport)

    def close(self):
        self.close_sftp()
        self.close_sftp()

    def close_sftp(self):
        if self.sftp:
            self.sftp.close()

    def close_ssh(self):
        if self.ssh:
            self.ssh.close()

    def get(self, remote_path: str, local_path: str):
        if self.sftp:
            return self.sftp.get(remotepath=remote_path, localpath=local_path)
        raise RuntimeError("No active sftp session opened!")

    def ls(self, remote_path: str):
        if self.sftp:
            return self.sftp.listdir(path=remote_path)
        raise RuntimeError("No active sftp session opened!")

    def put(self, local_path: str, remote_path: str):
        if self.sftp:
            return self.sftp.put(localpath=local_path, remotepath=remote_path)
        raise RuntimeError("No active sftp session opened!")
