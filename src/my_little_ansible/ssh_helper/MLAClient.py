import paramiko


class MLAClient(paramiko.SSHClient):
    ssh_mode: str = ""

    def __init__(self, ip: str, port: int, username: str, password: str, pkey_path: str = None):
        super().__init__()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.pkey = paramiko.RSAKey.from_private_key_file(pkey_path) if pkey_path is not None else None

    def __repr__(self):
        return "%s(ip=%r, port=%r, username=%r, password=%r, pkey=%r)" % \
               (self.__class__.__name__, self.ip, self.port, self.username, self.password, self.pkey)

    def __str__(self):
        return "%s(ip=%r, port=%r, username=%r, password=%r, pkey=%r)" % \
               (self.__class__.__name__, self.ip, self.port, self.username, self.password, self.pkey)
