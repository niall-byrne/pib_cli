"""ContainerSetupCommand class."""

import click
from pib_cli.support.container import installer

from .bases import command


class ContainerSetupCommand(command.CommandBase):
  """CLI command to setup a development container."""

  def invoke(self) -> None:
    """Invoke the command."""

    container_installer = installer.DevContainerInstaller()
    container_installer.container_valid_exception()
    container_installer.setup(click.echo)
