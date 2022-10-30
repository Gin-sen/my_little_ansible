import logging

from ..ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class BaseModule:
    name: str = "anonymous"
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

    @staticmethod
    def exec(ssh_client, commands):
        for cmd in commands:
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            stdin.write(f'{ssh_client.password}\n')
            stdin.flush()
            # print the results
            logger.debug(f"{ssh_client.username}@{ssh_client.hostname} STDOUT :\n{stdout.read().decode()}")
            logger.debug(f"{ssh_client.username}@{ssh_client.hostname} STDERR :\n{stderr.read().decode()}")

            stdin.close()
            stdout.close()
            stderr.close()
