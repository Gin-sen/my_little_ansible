"""template_module.py"""

import logging
import os
from stat import S_ISREG, S_ISLNK

from jinja2 import Environment, select_autoescape, FileSystemLoader
from .copy_module import CopyModule
from ..ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class TemplateModule(CopyModule):
    """class TemplateModule"""
    name: str = 'template'

    def __init__(self, params: dict):
        super().__init__(params)
        self.vars = params["vars"]
        logger.debug(f"template: {self.src}, dest: {self.dest}, vars={self.vars}")

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
        # Process Template
        if not os.path.isfile(self.src):
            raise FileNotFoundError

        logger.debug(f"Templating {self.src} with vars {self.vars}")
        env = Environment(
            loader=FileSystemLoader("."),
            autoescape=select_autoescape()
        )
        template = env.get_template(self.src)

        # Copy result
        out, err = super().exec(ssh_client,
                                [f"sudo -S chown {ssh_client.username}:{ssh_client.username}" +
                                 f" {os.path.dirname(self.dest)} {self.dest}"])
        logger.debug(f"chown {ssh_client.username}:{ssh_client.username} "
                     f"{os.path.dirname(self.dest)}")
        [logger.debug(o) for o in out]
        [logger.debug(r) for r in err]
        out, err = super().exec(ssh_client,
                                [f"sudo -S chmod o+rw {os.path.dirname(self.dest)} {self.dest}"])
        logger.debug(f"chmod a+rw {os.path.dirname(self.dest)} {self.dest}")
        [logger.debug(o) for o in out]
        [logger.debug(r) for r in err]
        with ssh_client.open_sftp() as sftp:
            self.discover_remote_dir_base(ssh_client, sftp, os.path.dirname(self.dest))
            self.listdir_and_write(sftp, os.path.dirname(self.dest), template.render(self.vars))

        ssh_client.close()

    def listdir_and_write(self, sftp, remote_dir, template):
        """
        Find file and write
        """
        for entry in sftp.listdir_attr(remote_dir):
            remote_path = remote_dir + "/" + entry.filename
            mode = entry.st_mode
            if remote_path != self.dest:
                logger.debug(f"remote_path {remote_path}!= self.dest = {self.dest}")
                continue
            logger.debug(f"remote_path = {remote_path} == self.dest = {self.dest}")
            if S_ISLNK(mode) or S_ISREG(mode):
                logger.debug(f"remote_path = {remote_path} is file or symbolic link")
                self.write_file(sftp, template, remote_path)
                logger.info(f"Write completed to {remote_path}")
        else:
            try:
                sftp.stat(self.dest)
                logger.debug(f"file exist, no need to create: {self.dest}")
            except IOError:
                logger.debug(f"create a file if it does not exist: {self.dest}")
                self.write_file(sftp, template, self.dest)
                logger.info(f"Write completed to {self.dest} (new file)")
