"""sysctl_module.py"""


import logging
import re

from .base_module import BaseModule
from ..ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class SysctlModule(BaseModule):
    """class systcl_module"""
    name: str = 'sysctl'

    def __init__(self, params: dict):
        super().__init__(params)
        self.attribute = params['attribute']
        self.value = params['value']
        self.permanent = params['permanent']

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

        if self.permanent:
            escaped_attrib = re.escape(self.attribute)
            escaped_value = re.escape(str(self.value))
            out, err = super().exec(ssh_client, [f'grep "^{escaped_attrib} = .*" '
                                                 f'/etc/sysctl.conf'])
            [logger.debug(o) for o in out]
            if out[0]:
                out, err = super().exec(ssh_client,
                                        [f'sudo -S sed -i -e '
                                         f'"s/^{escaped_attrib} = .*/'
                                         f'{escaped_attrib} = {escaped_value}/gm" '
                                         f'/etc/sysctl.conf'])
                [logger.debug(o) for o in out]
            else:
                logger.info(f"echo -e '{self.attribute} = {self.value}\\n'")
                out, err = super().exec(ssh_client,
                                        [f'sudo -S echo -e "{self.attribute} = {self.value}\n"'
                                         f' | sudo tee -a /etc/sysctl.conf'])
                [logger.debug(o) for o in out]
                [logger.debug(r) for r in err]
        else:
            out, err = super().exec(ssh_client,
                                    [f"sudo -S sysctl -w {self.attribute}={self.value}"])
            [logger.debug(o) for o in out]
            [logger.debug(r) for r in err]

        ssh_client.close()
