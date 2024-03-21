import locale

from .commander.cli import cli

locale.setlocale(locale.LC_ALL, "sk_SK.UTF-8")
cli()
