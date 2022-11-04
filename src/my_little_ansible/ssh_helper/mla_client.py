"""mla_client.py"""

import paramiko


class MlaClient(paramiko.SSHClient):
    """class mla"""
    ssh_mode: str = ""

    def __init__(self, ip_address: str, port: int,
                 username: str, password: str,
                 pkey_path: str = None,
                 hostname: str = None):
        super().__init__()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ip_address = ip_address
        self.port = port
        self.username = username
        self.password = password
        self.hostname = hostname
        self.pkey = paramiko.RSAKey.from_private_key_file(pkey_path) \
            if pkey_path is not None else None

    def __repr__(self):
        return f"{self.__class__.__name__}(ip_address={self.ip_address}," \
               f" port={self.port}, username={self.username}, " \
               f"password={self.password}, pkey={self.pkey}) "

    def __str__(self):
        return f"{self.__class__.__name__}(ip_address={self.ip_address}," \
               f" port={self.port}, username={self.username}, " \
               f"password={self.password}, pkey={self.pkey}) "
