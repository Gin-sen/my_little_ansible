"""SSH Management"""

import paramiko
import logging

__author__ = "deret_r, places_m"


def connection(hostname, port, key):
    """function to connect ssh"""
    k = paramiko.RSAKey.from_private_key_file(key)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username='mla_agent', password='mla_password', passphrase='', port=port, pkey=k)
    logging.info("connected")
    ssh.close()
