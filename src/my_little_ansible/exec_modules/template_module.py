import logging
import os

from paramiko import SSHClient

from .base_module import BaseModule
from .copy_module import CopyModule
from ..ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class TemplateModule(CopyModule):
    name: str = 'template'

    def __init__(self, params: dict):
        super().__init__(params)
        self.vars = params["vars"]
        logger.debug(f"template: {self.src}, dest: {self.dest}, vars={self.vars}")

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
        # Process Template
        if not os.path.isfile(self.src):
            raise FileNotFoundError
        logger.debug(f"Templating {self.src} with vars {self.vars}")
        # Copy result
        self.copy(ssh_client)

        ssh_client.close()
        pass
