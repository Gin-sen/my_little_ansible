import logging


from .base_module import BaseModule
from ..ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class AptModule(BaseModule):
    name: str = 'package-name'
    state: str = 'undefined'

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
        logger.info("connected")
        ssh_client.close()
        pass
