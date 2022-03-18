"""ConfigVersionCommand class."""

import click
from pib_cli.config.locale import _

from .bases import command_config


class ConfigVersionCommand(command_config.CommandConfigBase):
  """CLI command to validate the current PIB CLI configuration."""

  def invoke(self) -> None:
    """Invoke the command."""

    user_config = self.user_config_file.parse()
    click.echo(
        _(
            "Configuration file: {path}\n"
            "Configuration version: {version}"
        ).format(
            path=self.user_config_file.get_config_file_name(),
            version=user_config.version,
        )
    )
