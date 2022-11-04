"""base_module.py"""

import logging

from ..ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class BaseModule:
    """class base_module"""
    name: str = "anonymous"
    state: str = "unknown"

    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client: MlaClient, ssh_mode: str):
        """
        Apply the action to `ssh_client` using `params`.

        Args:
            ssh_client (MLAClient):
            ssh_mode (str):
        """
        ssh_client.connect(hostname=ssh_client.ip_address,
                           port=ssh_client.port,
                           username=ssh_client.username,
                           pkey=ssh_client.pkey)
        logger.info("connected")
        ssh_client.close()

    @staticmethod
    def exec(ssh_client, commands):
        """
        execute list of commands in ssh_client
        """
        out, err = ([], [])
        for cmd in commands:
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            stdin.write(f'{ssh_client.password}\n')
            stdin.flush()
            out.append(stdout.read().decode())
            err.append(stderr.read().decode())
            stdin.close()
            stdout.close()
            stderr.close()
        return out, err
