"""ConfigValidateCommand class."""

import click
from pib_cli.config.locale import _

from .bases import command_config


class ConfigValidateCommand(command_config.CommandConfigBase):
  """CLI command to validate a PIB CLI configuration file."""

  def invoke(self) -> None:
    """Invoke the command."""

    user_config = self.user_config_file.parse()
    click.echo(
        _(
            "Configuration file: {path}\n"
            "This configuration is valid.").format(
                name=user_config.get_project_name(),
                path=self.user_config_file.get_config_file_name(),
            )
    )
