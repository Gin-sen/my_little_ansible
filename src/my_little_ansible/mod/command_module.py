"""command_module.py"""


import logging

from .base_module import BaseModule

from ..ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class CommandModule(BaseModule):
    """class CommandModule"""
    name: str = 'command'

    def __init__(self, params: dict):
        super().__init__(params)
        self.command = params['command']

    def process(self, ssh_client: MlaClient, ssh_mode: str):
        """
        Apply the action to `ssh_client` using `params`.

        Args:
            ssh_client (MlaClient):
            ssh_mode (str):
        """
        ssh_client.connect(hostname=ssh_client.ip_address,
                           port=ssh_client.port,
                           username=ssh_client.username,
                           pkey=ssh_client.pkey)
        logger.info(f"Connected to {ssh_client.username}@{ssh_client.hostname}")

        commands = []
        commands.append(self.command)
        out, err = super().exec(ssh_client, commands)

        for command, output_line, error_line in zip(commands[0].split('\n'), out, err):
            logger.info(f"Command : {command}")
            if output_line:
                logger.info(f"Output :\n{output_line}")
            if error_line:
                logger.debug(error_line)

        ssh_client.close()
