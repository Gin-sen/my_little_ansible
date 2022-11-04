"""host.py"""


class Host:
    """host class"""

    def __init__(self, name: str, ip_address: str, port: int, ssh_mode: str = "",
                 pkey_path: str = "/home/vagrant/mla_key",
                 username: str = "mla_agent", password: str = "mla_password"):
        """

        Args:
            name (str):
            ip_address (str):
            port (str):
            ssh_mode (str):
            pkey_path (str):
            username (str):
            password (str):
        """
        self.name = name
        self.ip_address = ip_address
        self.port = port
        self.ssh_mode = ssh_mode
        self.pkey_path = pkey_path
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}," \
               f" ip_address={self.ip_address}," \
               f" port={self.port})"

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}," \
               f" ip_address={self.ip_address}," \
               f" port={self.port})"
