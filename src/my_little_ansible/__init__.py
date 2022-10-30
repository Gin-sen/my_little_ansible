import sys

import click
import logging

from .MLA import MLA
from .models import parse_inventory, parse_todos
from .ssh_helper.ssh_management import connection

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stderr_handler = logging.FileHandler('error.log')
stderr_handler.setLevel(logging.ERROR)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)

handlers = [stderr_handler, stdout_handler]
formatter = logging.Formatter('%(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s')
for handler in handlers:
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@click.command()
@click.option('-f', show_default=True, default="todos.yml", help='instruction file (default: todos.yml)')
@click.option('-i', show_default=True, default="inventory.yml", help='models file (default: inventory.yml)')
@click.option('--debug', is_flag=True, show_default=True, default=False, help='debug mode (default: False)')
@click.option('--dry-run', is_flag=True, show_default=True, default=False, help='dry-run mode (default: False)')
@click.option('--dev', is_flag=True, show_default=True, default=True, help='dev mode (default: True)')
def init_click_cmd(f, i, debug, dry_run, dev):
    """
    Main function
    :param dev:
    :param f:
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
    mla = MLA(parse_inventory(i), parse_todos(f))
    logger.debug("          Files parsed ✅")
    logger.info("Processing %i tasks on hosts: %s" % (len(mla.todos), "%s" % ", ".join(mla.get_hosts_ip())))
    if not dry_run:
        mla.run()
    else:
        mla.dry_run()
