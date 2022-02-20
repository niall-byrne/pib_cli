"""Built in CLI configuration commands."""

import click
from pib_cli.cli.commands import config_show, config_where, handler


@click.group('config')
def config() -> None:
  """PIB user configuration commands."""


@config.command("show")
def show_config_builtin() -> None:
  """Display the current CLI configuration."""

  handler(config_show.ConfigShowCommand)


@config.command("where")
def where_config_builtin() -> None:
  """Display the current CLI configuration location."""

  handler(config_where.ConfigWhereCommand)


config_commands: click.Command = config
