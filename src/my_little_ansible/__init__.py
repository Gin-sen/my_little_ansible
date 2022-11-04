"""__init__.py"""
import string
import sys

import logging
import click

from .mla import Mla
from .models import parse_inventory, parse_todos

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stderr_handler = logging.FileHandler('error.log')
stderr_handler.setLevel(logging.ERROR)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)

handlers = [stderr_handler, stdout_handler]
new_format_str = '[{asctime},{msecs:3.0f}] {name:38s} [{levelname:^8s}] {message}'
formatter = logging.Formatter(new_format_str, style="{",
                              datefmt='%Y-%m-%d %H:%M:%S')
for handler in handlers:
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@click.command()
@click.option('-f',
              '--file_todo',
              show_default=True,
              default="todos.yml",
              help='instruction file (default: todos.yml)')
@click.option('-i',
              show_default=True,
              default="inventory.yml",
              help='models file (default: inventory.yml)')
@click.option('--debug',
              is_flag=True,
              show_default=True,
              default=False,
              help='debug mode (default: False)')
@click.option('--dry-run',
              is_flag=True,
              show_default=True,
              default=False,
              help='dry-run mode (default: False)')
@click.option('--dev',
              is_flag=True,
              show_default=True,
              default=False,
              help='dev mode (default: True)')
def init_click_cmd(file_todo, i, debug, dry_run, dev):
    """
    Main function
    :param dev:
    :param file_todo:
    :param i:
    :param debug:
    :param dry_run:
    """
    if dev:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if debug:
        logger.debug("Activer l'affichage des stack traces")
    my_mla = Mla(parse_inventory(i), parse_todos(file_todo))
    logger.debug("Files parsed ✅ ")
    logger.info(f"Processing {len(my_mla.todos)} tasks on hosts: {', '.join(my_mla.get_hosts_ip())}")
    if not dry_run:
        my_mla.run()
    else:
        my_mla.dry_run()
