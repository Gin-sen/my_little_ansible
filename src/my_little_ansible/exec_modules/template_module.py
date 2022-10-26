import logging

from paramiko import SSHClient

from .base_module import BaseModule
from ..ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class TemplateModule(BaseModule):
    name: str = 'template'

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
        ssh_client.close()
        pass
