"""ConfigValidateCommand class."""

import click
from pib_cli.support import user_configuration

from .bases import command


class ConfigValidateCommand(command.CommandBase):
  """CLI command to validate the current PIB CLI configuration."""

  def invoke(self) -> None:
    """Invoke the command."""

    configuration = user_configuration.UserConfiguration()
    configuration.validate()

    click.echo("Current configuration is valid.")
