
class Host:
    def __init__(self, name: str, ip: str, port: int, ssh_mode: str = "", pkey_path: str = "/home/vagrant/mla_key",
                 username: str = "mla_agent", password: str = "mla_password"):
        """

        Args:
            name (str):
            ip (str):
            port (str):
            ssh_mode (str):
            pkey_path (str):
            username (str):
            password (str):
        """
        self.name = name
        self.ip = ip
        self.port = port
        self.ssh_mode = ssh_mode
        self.pkey_path = pkey_path
        self.username = username
        self.password = password

    def __repr__(self):
        return "%s(name=%r, ip=%r, port=%r)" % (self.__class__.__name__, self.name, self.ip, self.port)

    def __str__(self):
        return "%s %r (%r:%r)" % (self.__class__.__name__, self.name, self.ip, self.port)
