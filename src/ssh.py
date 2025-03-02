import paramiko


class SshClient:
    host: str
    port: int
    username: str
    password: str
    ssh: paramiko.SSHClient
    sftp: paramiko.SFTPClient

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
            allow_agent=False,
            look_for_keys=False
        )

    def connect_sftp(self):
        if self.ssh:
            self.sftp = self.ssh.open_sftp()

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
