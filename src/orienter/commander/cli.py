import os
import subprocess

import click

from ..configurator.constants import CONFIG_FILE_PATH


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        from .menu import Menu

        Menu.main_menu()
        return


@cli.command()
def configure():
    editor = os.environ.get("EDITOR")
    if not editor:
        editor = "vi"
        print("Premenná prostredia $EDITOR nie je nastavená! Pokúsim sa použiť vi.")
    subprocess.call((editor, CONFIG_FILE_PATH))


if __name__ == "__main__":
    cli()
