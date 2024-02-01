import os
import subprocess

import click

from .menu import Menu
from ..configurator import CONFIG_FILE_PATH


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        Menu.main_menu()
        return


@cli.command()
def configure():
    editor = os.environ.get('EDITOR')
    subprocess.call((editor, CONFIG_FILE_PATH))


if __name__ == "__main__":
    cli()
