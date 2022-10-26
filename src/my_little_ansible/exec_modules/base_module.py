import logging

from ..ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class BaseModule:
    name: str = "anonymous"
    state: str = "unknown"
    state: str = "unknown"

    def __init__(self, params: dict):
        self.params = params

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
