"""ConfigValidateCommand class."""

import click
from pib_cli.config.locale import _
from pib_cli.support import state

from .bases import command


class ConfigValidateCommand(command.CommandBase):
  """CLI command to validate the current PIB CLI configuration."""

  def invoke(self) -> None:
    """Invoke the command."""

    loaded_configuration = state.State()
    loaded_configuration.user_config.validate()

    click.echo(_("Current configuration is valid."))
