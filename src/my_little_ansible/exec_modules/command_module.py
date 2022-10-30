import logging

from .base_module import BaseModule
from paramiko import SSHClient

from ..ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class CommandModule(BaseModule):
    name: str = 'command'

    def __init__(self, params: dict):
        super().__init__(params)
        self.command = params['command']

    def process(self, ssh_client: MLAClient, ssh_mode: str):
        """
        Apply the action to `ssh_client` using `params`.

        Args:
            ssh_client (MLAClient):
            ssh_mode (str):
        """
        ssh_client.connect(hostname=ssh_client.ip, port=ssh_client.port, username=ssh_client.username,
                           pkey=ssh_client.pkey)
        logger.info("connected")

        commands = []
        commands.append(self.command)
        super(CommandModule, self).exec(ssh_client, commands)

        ssh_client.close()
        pass
