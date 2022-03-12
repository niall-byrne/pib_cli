"""ConfigWhereCommand class."""

import click
from pib_cli.config.locale import _

from .bases import command_config


class ConfigWhereCommand(command_config.CommandConfigBase):
  """CLI command to locate a PIB CLI configuration file."""

  def invoke(self) -> None:
    """Invoke the command."""

    click.echo(
        _("Configuration file: {config_filename}").format(
            config_filename=self.user_config_file.get_config_file_name()
        )
    )
