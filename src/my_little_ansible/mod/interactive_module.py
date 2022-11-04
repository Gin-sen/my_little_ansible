"""interactive_module.py"""
import logging
import sys
import traceback

from my_little_ansible.ssh_helper import interactive
from my_little_ansible.mod.base_module import BaseModule
from my_little_ansible.ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class InteractiveModule(BaseModule):
    """class interactive_module"""
    name: str = 'interactive_module'
    shell: str = 'bash'

    def __init__(self, params: dict):
        super().__init__(params)
        # self.name = params['name']
        #self.shell = params['shell']

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

        # now, connect and use paramiko Client to negotiate SSH2 across the connection
        try:

            chan = ssh_client.invoke_shell()
            logger.info(repr(ssh_client.get_transport()))
            logger.info("*** Here we go!\n")
            interactive.interactive_shell(chan)
            chan.close()
            ssh_client.close()

        except Exception as exception:
            logger.info(f"*** Caught exception: {exception.__class__}: {exception}")
            traceback.print_exc()
            try:
                ssh_client.close()
            except OSError:
                pass
            sys.exit(1)
