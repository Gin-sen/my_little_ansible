import logging
import os

from .exec_modules.apt_module import AptModule
from .exec_modules.base_module import BaseModule
from .exec_modules.command_module import CommandModule
from .exec_modules.copy_module import CopyModule
from .exec_modules.service_module import ServiceModule
from .exec_modules.sysctl_module import SysctlModule
from .exec_modules.template_module import TemplateModule
from .models import Host, Todo
from .ssh_helper.MLAClient import MLAClient

logger = logging.getLogger(__name__)


class MLA:

    def __init__(self, hosts: [Host], todos: [Todo]):
        """

        :type todos: [Todo]
        :type hosts: [Host]
        """
        self.hosts = hosts
        self.todos = todos
        self.modules = self.get_modules()
        self.ssh_clients = self.get_ssh_clients()
        # Init logging but in class logger
        # logger.info("Processing %i tasks on hosts: %s" % (len(self.todos), "%s" % ", ".join(self.get_hosts_ip())))

    def __repr__(self):
        return "%s(hosts=%r, todos=%r, ssh_clients=%r, modules=%r)" % (self.__class__.__name__, self.hosts, self.todos,
                                                                       self.ssh_clients, self.modules)

    def get_hosts_ip(self) -> [str]:
        """
        Returns Hosts IP Address
        :return:
        """
        ip = []
        for host in self.hosts:
            ip.append(host.ip)
        return ip

    def get_modules(self):
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
                case _:
                    logger.warning("BaseModule used : Unclear behavior expected !")
                    modules.append(BaseModule(todo.params))
        return modules

    def get_ssh_clients(self):
        ssh_clients = []
        for host in self.hosts:
            match host.ssh_mode:
                case ["pkey"]:
                    if os.path.isfile(host.pkey_path):
                        ssh_clients.append(MLAClient(host.ip, host.port,
                                                     "mla_agent", "mla_password", host.pkey_path, hostname=host.name))
                    else:
                        raise FileNotFoundError(host.pkey_path)
                case ["login"]:
                    ssh_clients.append(MLAClient(host.ip, host.port,
                                                 host.username, host.password, hostname=host.name))
                case _:
                    ssh_clients.append(MLAClient(host.ip, host.port,
                                                 "mla_agent", "mla_password", "/home/vagrant/.ssh/mla_key",
                                                 hostname=host.name))
        return ssh_clients

    def dry_run(self):
        for (host, client) in zip(self.hosts, self.ssh_clients):
            logger.debug(client)
            logger.debug(host)
            for (todo, task) in zip(self.todos, self.modules):
                logger.debug(task)
                logger.debug(todo)

    def run(self):
        for (host, client) in zip(self.hosts, self.ssh_clients):
            for (todo, task) in zip(self.todos, self.modules):
                logger.info(f"Running {todo} on {host}")
                task.process(client, host.ssh_mode)
