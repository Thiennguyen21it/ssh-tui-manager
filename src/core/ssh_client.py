import os
import paramiko
from typing import Optional, Tuple
from .host_manager import SSHHost

class SSHClient:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, host: SSHHost) -> Tuple[bool, str]:
        """Connect to an SSH host."""
        try:
            kwargs = {
                'hostname': host.host,
                'username': host.user,
                'port': host.port,
            }
            
            if host.key_path and os.path.exists(host.key_path):
                kwargs['key_filename'] = host.key_path
            
            self.client.connect(**kwargs)
            return True, "Connected successfully"
        except Exception as e:
            return False, str(e)

    def disconnect(self):
        """Disconnect from the current SSH session."""
        if self.client:
            self.client.close()

    def execute_command(self, command: str) -> Tuple[int, str, str]:
        """Execute a command on the remote host."""
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            return exit_code, stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            return -1, "", str(e)

    def scp_upload(self, local_path: str, remote_path: str) -> Tuple[bool, str]:
        """Upload a file to the remote host."""
        try:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            return True, "File uploaded successfully"
        except Exception as e:
            return False, str(e)

    def scp_download(self, remote_path: str, local_path: str) -> Tuple[bool, str]:
        """Download a file from the remote host."""
        try:
            sftp = self.client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            return True, "File downloaded successfully"
        except Exception as e:
            return False, str(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect() 