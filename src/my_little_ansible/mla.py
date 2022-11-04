"""mla.py"""
import logging
import os
from .mod.apt_module import AptModule
from .mod.base_module import BaseModule
from .mod.command_module import CommandModule
from .mod.copy_module import CopyModule
from .mod.interactive_module import InteractiveModule
from .mod.service_module import ServiceModule
from .mod.sysctl_module import SysctlModule
from .mod.template_module import TemplateModule
from .models import Host, Todo
from .ssh_helper.mla_client import MlaClient

logger = logging.getLogger(__name__)


class Mla:
    """Mla class"""
    def __init__(self, hosts: [Host], todos: [Todo]):
        """

        :type todos: [Todo]
        :type hosts: [Host]
        """
        self.hosts = hosts
        self.todos = todos
        self.modules = self.get_modules()
        self.ssh_clients = self.get_ssh_clients()

    def __repr__(self):
        return f"(hosts={self.__class__.__name__}," \
               f" todos={self.hosts}," \
               f" ssh_clients={self.ssh_clients}," \
               f" modules={self.modules}) "

    def get_hosts_ip(self) -> [str]:
        """
        Returns Hosts IP Address
        :return:
        """
        ip_address = []
        for host in self.hosts:
            ip_address.append(host.ip_address)
        return ip_address

    def get_modules(self):
        """
        Returns Modules
        :return:
        """
        modules = []
        for todo in self.todos:
            match todo.name:
                case "apt":
                    modules.append(AptModule(todo.params))
                case "copy":
                    modules.append(CopyModule(todo.params))
                case "command":
                    modules.append(CommandModule(todo.params))
                case "service":
                    modules.append(ServiceModule(todo.params))
                case "sysctl":
                    modules.append(SysctlModule(todo.params))
                case "template":
                    modules.append(TemplateModule(todo.params))
                case "interactive":
                    modules.append(InteractiveModule(todo.params))
                case _:
                    logger.warning("BaseModule used : Unclear behavior expected !")
                    modules.append(BaseModule(todo.params))
        return modules

    def get_ssh_clients(self):
        """
        Returns ssh_client
        :return:
        """
        ssh_clients = []
        for host in self.hosts:
            match host.ssh_mode:
                case ["pkey"]:
                    if os.path.isfile(host.pkey_path):
                        ssh_clients.append(MlaClient(host.ip_address,
                                                     host.port,
                                                     "mla_agent",
                                                     "mla_password",
                                                     host.pkey_path, hostname=host.name))
                    else:
                        raise FileNotFoundError(host.pkey_path)
                case ["login"]:
                    ssh_clients.append(MlaClient(host.ip_address, host.port,
                                                 host.username, host.password, hostname=host.name))
                case _:
                    ssh_clients.append(MlaClient(host.ip_address, host.port,
                                                 "mla_agent", "mla_password",
                                                 "/home/vagrant/.ssh/mla_key",
                                                 hostname=host.name))
        return ssh_clients

    def dry_run(self):
        """
        logger
        """
        for (host, client) in zip(self.hosts, self.ssh_clients):
            for (todo, task) in zip(self.todos, self.modules):
                logger.info(f"Should run Task {task.__class__.__name__} on {host}")

    def run(self):
        """
        runner
        """
        for (host, client) in zip(self.hosts, self.ssh_clients):
            for (todo, task) in zip(self.todos, self.modules):
                logger.info(f"Running Task {task.__class__.__name__} on {host}")
                task.process(client, host.ssh_mode)
                logger.info(f"Task {task.__class__.__name__} on {host} completed ✅ ")
