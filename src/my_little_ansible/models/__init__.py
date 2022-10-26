
import logging
import os

import yaml

from .Host import Host
from .Todo import Todo


logger = logging.getLogger(__name__)


def parse_inventory(inventory_file):
    """
    Inventory parser
    :param inventory_file:
    :return:
    """
    hosts: list[Host] = []
    try:
        if os.path.isfile(inventory_file):
            with open(inventory_file, "r") as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                for host in list(data['hosts'].keys()):
                    hosts.append(Host(host, data['hosts'][host]['ssh_address'], data['hosts'][host]['ssh_port']))
                file.close()
        else:
            logger.error("Inventory file does not exist")
            raise FileNotFoundError(inventory_file)
    except():
        logging.error("Error while parsing models file")
    return hosts


def parse_todos(todos_file):
    """
    Todos parser
    :param todos_file:
    :return:
    """
    todos: list[Todo] = []
    try:
        if os.path.isfile(todos_file):
            with open(todos_file, "r") as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                for todo in data:
                    todos.append(Todo(todo['module'], todo['params']))
                file.close()
        else:
            logging.error("Todos file does not exist")
    except():
        logging.error("Error while parsing models file")
    return todos
