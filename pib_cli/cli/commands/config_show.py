"""ConfigShowCommand class."""

import click
from pib_cli.support import state

from .bases import command


class ConfigShowCommand(command.CommandBase):
  """CLI command to report the PIB CLI version."""

  def invoke(self) -> None:
    """Invoke the command."""

    loaded_configuration = state.State()
    click.echo(loaded_configuration.user_config.get_raw_file())
