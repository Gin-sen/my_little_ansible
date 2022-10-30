import logging
import os
import stat
import time
from stat import S_ISDIR

import paramiko
from paramiko.util import get_logger

from .base_module import BaseModule
from ..ssh_helper.MLAClient import MLAClient
from ..ssh_helper.MLAFTPClient import MLAFTPClient

logger = logging.getLogger(__name__)
logger = get_logger(__name__)


class CopyModule(BaseModule):
    name: str = 'copy'

    def __init__(self, params: dict):
        super().__init__(params)
        self.state = "starting"
        self.src = params['src']
        # Handling dest ending by /
        if params['dest'].endswith("/"):
            self.dest = params['dest'][:-1]
        else:
            self.dest = params['dest']
        self.backup = params['backup']

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
        self.copy(ssh_client)
        ssh_client.close()
        pass

    def copy(self, ssh_client):
        sftp = ssh_client.open_sftp()
        logger.info(f"SFTP opened to {ssh_client.username}@{ssh_client.hostname}")
        logger.info(f"Transferring {self.src} to {self.dest} :")
        super(self.__class__, self).exec(ssh_client, [f"sudo -S chown {ssh_client.username}:{ssh_client.username}"
                                                      f" {os.path.dirname(self.dest)}"])
        logger.info(f"Creating dir : {self.dest}")
        self.mkdir(sftp, self.dest, ignore_existing=True)
        self.put_dir(sftp, self.src, self.dest)
        sftp.close()

    def put_dir(self, sftp, source, target):
        """ Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        """
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                logger.debug(f"Putting file {os.path.join(source, item)} in {os.path.join(target, item)}")
                sftp.put(os.path.join(source, item), os.path.join(target, item), confirm=False)
            else:
                logger.debug(f"Creating folder {os.path.join(target, item)}")
                self.mkdir(sftp, os.path.join(target, item), ignore_existing=True)
                self.put_dir(sftp, os.path.join(source, item), os.path.join(target, item))

    @staticmethod
    def mkdir(sftp, path, mode=511, ignore_existing=False):
        """ Augments mkdir by adding an option to not fail if the folder exists  """
        try:
            logger.debug(f"mkdir : {path}")
            sftp.mkdir(path, mode)
        except IOError:
            if ignore_existing:
                logger.debug(f"IOError but ignoring (ignore_existing flag) : {IOError}")
                logger.debug(f"Possible reason : {path} might already exists")
            else:

                raise

