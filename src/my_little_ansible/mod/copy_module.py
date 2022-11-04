"""copy_module.py"""


import logging
import os
import stat

from paramiko.sftp_client import SFTPClient

from .base_module import BaseModule
from ..ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class CopyModule(BaseModule):
    """class CopyModule"""
    name: str = 'copy'

    def __init__(self, params: dict):
        super().__init__(params)
        self.state = "starting"
        self.src = params['src']
        # Handling dest ending by /
        self.dest = params['dest'][:-1] if params['dest'].endswith("/") else params['dest']
        # default value & data validation
        self.backup = params['backup']  \
            if 'backup' in params and isinstance(params['backup'], bool)\
            else True

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
        with ssh_client.open_sftp() as sftp:
            # build remote dir
            self.discover_remote_dir_base(ssh_client, sftp, self.dest)
            # walk local source
            for root, dirs, files in os.walk(self.src):
                for name in files:
                    relative_remote_path = \
                        os.path.join(self.dest,
                                     *os.path.join(root, name).split('/')[2:])
                    logger.debug(f"File (put {os.path.join(root, name)} to {relative_remote_path})")
                    sftp.put(os.path.join(root, name), relative_remote_path)
                for name in dirs:
                    relative_remote_path = os\
                        .path.join(self.dest,
                                   *os.path.join(root,
                                                 name).split('/')[2:])
                    try:
                        logger.debug(f"Dir (mkdir to {relative_remote_path})")
                        sftp.mkdir(relative_remote_path)
                    except IOError:
                        logger.debug(f"Dir {relative_remote_path} might already exist")

        ssh_client.close()

    def discover_remote_dir_base(self, ssh_client, sftp, remote_path, is_recursive: bool = False):
        """
        recursive discover directory
        """
        try:
            for file_attr in sftp.listdir_attr(remote_path):
                if stat.S_ISDIR(file_attr.st_mode):
                    logger.debug(f"It's a directory : {remote_path}")
                    logger.debug(f"Can create or chmod recursively "
                                 f"{self.dest} in {remote_path} ? {is_recursive}")
                    break
                elif stat.S_ISREG(file_attr.st_mode):
                    logger.debug(f"It's a file : {remote_path}/{file_attr.filename}")
                    pass
            if is_recursive:
                self.make_recurse_dir_base(ssh_client, sftp, remote_path, self.dest)
            logger.debug(f"Directory exists : {remote_path}")
        except IOError as io_error:
            if io_error.errno == 2:
                logger.debug(f"ENOENT 2 No such file or directory : {remote_path}")
                logger.debug(f"Recurse to create parent directory : {os.path.dirname(remote_path)}")
                self.discover_remote_dir_base(ssh_client, sftp, os.path.dirname(remote_path), True)
            else:
                logger.debug(f"ENOENT {io_error.errno} : {remote_path}")

    def make_recurse_dir_base(self, ssh_client, sftp, from_remote_base, to_final_remote):
        """
        create folders recursively
        """
        relative_path_to_create = os.path.relpath(to_final_remote, from_remote_base)
        logger.debug(f"from_remote_base : {from_remote_base}")
        logger.debug(f"to_final_remote : {to_final_remote}")
        logger.debug(f"Relative path : {relative_path_to_create}")
        history = ""
        for new_dir in relative_path_to_create.split('/'):
            history += new_dir
            try:
                sftp.mkdir(os.path.join(from_remote_base, history))
                logger.debug(f"Folder {os.path.join(from_remote_base, history)} created")
                super().exec(ssh_client,
                                                 [f"sudo -S chmod o+rw "
                                                  f"{os.path.join(from_remote_base, history)}"])
                logger.debug(f"Folder {os.path.join(from_remote_base, history)} chmod o+wr")

            except IOError as io_error:
                if io_error.errno == 13:
                    logger.debug(f"ENOENT 13 Permission denied : "
                                 f"{os.path.join(from_remote_base, history)}")
                    logger.debug(f"Directory {from_remote_base} exists but must be chmod o+rw")
                    out, err = super().\
                        exec(ssh_client,
                        [f"sudo -S chmod o+rw {from_remote_base}",
                         f"sudo -S chown {ssh_client.username}:"
                         f"{ssh_client.username} {from_remote_base}"])
                    [logger.debug(o) for o in out]
                    [logger.debug(r) for r in err]
                    self.make_recurse_dir_base(ssh_client, sftp,
                                               from_remote_base, to_final_remote)
                if io_error.errno == 2:
                    logger.debug(f"ENOENT 2 Directory does not exist : "
                                 f"{os.path.join(from_remote_base, history)}")
                    self.make_recurse_dir_base(ssh_client, sftp,
                                               os.path.join(from_remote_base, history),
                                               to_final_remote)

            history += '/'

    @staticmethod
    def write_file(sftp: SFTPClient, template_str, target):
        """
            Uploads the contents of the source directory to the target path. The
            target directory needs to exist. All subdirectories in source are
            created under target.
        """
        file_stream = sftp.open(target, 'w')
        file_stream.write(template_str)
        file_stream.close()
