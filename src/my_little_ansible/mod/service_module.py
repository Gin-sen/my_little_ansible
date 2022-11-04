"""service_module.py"""

import logging

from .base_module import BaseModule
from ..ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class ServiceModule(BaseModule):
    """class ServiceModule"""
    name: str = 'service'

    def __init__(self, params: dict):
        super().__init__(params)
        self.service = params['name']
        match params["state"]:
            case "started":
                self.arg = "start"
            case "restarted":
                self.arg = "restart"
            case "stopped":
                self.arg = "stop"
            case "enabled":
                self.arg = "enable"
            case "disabled":
                self.arg = "disable"
            case "status":
                self.arg = "status"
            case _:
                self.arg = "status"

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

        super().exec(ssh_client,
                     [f"sudo -S systemctl {self.arg}"
                      f" {self.service}"])
        logger.info(f"Service {self.service} command {self.arg} : Success")
        out, _ = super().exec(ssh_client,
                              [f"sudo -S systemctl is-active {self.service}",
                               f"sudo -S systemctl is-enabled {self.service}"])
        is_active = out[0]
        is_enabled = out[1]

        logger.info(f"Service {self.service} is {is_active[:-1]} and {is_enabled[:-1]}")

        ssh_client.close()
