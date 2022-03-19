"""ContainerSetupCommand class."""

import click
from pib_cli.config.locale import _
from pib_cli.support.container import exceptions, installer

from .bases import command


class ContainerSetupCommand(command.CommandBase):
  """CLI command to setup a development container."""

  def invoke(self) -> None:
    """Invoke the command."""

    try:
      container_installer = installer.DevContainerInstaller()
      container_installer.container_valid_exception()
      container_installer.setup(click.echo)
    except exceptions.DevContainerException as exc:
      click.echo(
          _("ERROR: {container_error}").format(container_error=exc.args[0])
      )
      exc.exit()
