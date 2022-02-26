"""Built in CLI configuration commands."""

import click
from pib_cli.cli.commands import (
    config_show,
    config_validate,
    config_where,
    handler,
)
from pib_cli.config.locale import _


@click.group(_("config"))
def config() -> None:
  """PIB user configuration commands."""


@config.command(_("show"))
def show_config_builtin() -> None:
  """Display the current CLI configuration."""

  handler(config_show.ConfigShowCommand)


@config.command(_("validate"))
def validate_config_builtin() -> None:
  """Validate the current CLI configuration."""

  handler(config_validate.ConfigValidateCommand)


@config.command(_("where"))
def where_config_builtin() -> None:
  """Display the current CLI configuration location."""

  handler(config_where.ConfigWhereCommand)


config_commands: click.Command = config
