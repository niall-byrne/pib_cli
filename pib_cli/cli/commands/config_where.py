"""ConfigWhereCommand class."""

import click
from pib_cli import config_filename
from pib_cli.config.locale import _

from .bases import command


class ConfigWhereCommand(command.CommandBase):
  """CLI command to reveal the current PIB CLI configuration's location."""

  def invoke(self) -> None:
    """Invoke the command."""

    click.echo(
        _("Current Configuration: {config_filename}").format(
            config_filename=config_filename
        )
    )
