"""ConfigShowCommand class."""

import click

from .bases import command_config


class ConfigShowCommand(command_config.CommandConfigBase):
  """CLI command to show the contents of a PIB CLI configuration file."""

  def invoke(self) -> None:
    """Invoke the command."""

    click.echo(self.user_config_file.get_raw_file())
