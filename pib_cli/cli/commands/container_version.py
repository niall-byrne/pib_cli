"""ContainerVersionCommand class."""

import click
from pib_cli.config.locale import _
from pib_cli.support import container
from pib_cli.support.container import exceptions

from .bases import command


class ContainerVersionCommand(command.CommandBase):
  """CLI command to report the current container version."""

  def invoke(self) -> None:
    """Invoke the command."""

    development_container = container.DevContainer()

    try:
      version_data = development_container.get_container_version()
      click.echo(
          _("Detected PIB container version: {version_data}").format(
              version_data=version_data
          )
      )
    except exceptions.DevContainerException:
      click.echo(_("No PIB container found."))
