"""VersionCommand class."""

import click
import pkg_resources
from pib_cli.config.locale import _

from .bases import command


class VersionCommand(command.CommandBase):
  """CLI command to report the PIB CLI version."""

  def invoke(self) -> None:
    """Invoke the command."""

    version_data = pkg_resources.get_distribution('pib_cli').version
    click.echo(
        _("pib_cli version: {version_data}").format(version_data=version_data),
    )
