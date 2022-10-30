import logging

from paramiko import SSHClient

from .base_module import BaseModule
from ..ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class SysctlModule(BaseModule):
    name: str = 'sysctl'

    def __init__(self, params: dict):
        super().__init__(params)
        self.name = params['name']
        self.state = params['state']

    def process(self, ssh_client: MLAClient, ssh_mode: str):
        """
        Apply the action to `ssh_client` using `params`.

        Args:
            ssh_client (MLAClient):
            ssh_mode (str):
        """
        ssh_client.connect(hostname=ssh_client.ip, port=ssh_client.port, username=ssh_client.username,
                           pkey=ssh_client.pkey)
        logger.info(f"Connected to {ssh_client.username}@{ssh_client.hostname}")

        commands = []
        commands.append("sudo -S apt-get update")
        commands.append(f"sudo -S apt-get install -{self.name}")

        super(SysctlModule, self).exec(ssh_client, commands)
        ssh_client.close()
        pass
