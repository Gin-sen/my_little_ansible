"""apt_module.py"""

import logging

from .base_module import BaseModule
from ..ssh_helper.mla_client import MlaClient


logger = logging.getLogger(__name__)


class AptModule(BaseModule):
    """class AptModule"""
    name: str = 'package-name'
    state: str = 'present'

    def __init__(self, params: dict):
        super().__init__(params)
        self.name = params['name']
        self.state = params['state']

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
        logger.info(f"Connected to {ssh_client.username}@{ssh_client.hostname}")

        out, _ = super().exec(ssh_client,
                              [f"sudo -S apt list {self.name} --installed"])
        commands = []
        commands.append("sudo -S apt-get update")
        match self.state:
            case "absent" if "installed" in out[0]:
                logger.info(f"Package {self.name} installed and must be uninstalled")
                commands.append(f"sudo -S apt-get purge -y {self.name}")
            case "present" if "installed" not in out[0]:
                logger.info(f"Package {self.name} not present and must be installed")
                commands.append(f"sudo -S apt-get install -y {self.name}")
            case "present" if "installed" in out[0]:
                logger.info(f"Package {self.name} already present")
            case "absent" if "installed" not in out[0]:
                logger.info(f"Package {self.name} already absent")
            case _:
                logger.info(f"Package {self.name} must not be uninstalled (by default)")
                commands.append(f"sudo -S apt-get install -y {self.name}")

        super().exec(ssh_client, commands)
        ssh_client.close()
