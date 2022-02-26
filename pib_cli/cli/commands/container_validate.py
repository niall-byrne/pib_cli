"""ContainerValidateCommand class."""

import sys

import click
from pib_cli.config.locale import _
from pib_cli.support import container
from pib_cli.support.container import exceptions

from .bases import command


class ContainerValidateCommand(command.CommandBase):
  """CLI command to validate the current container."""

  def invoke(self) -> None:
    """Invoke the command."""

    development_container = container.DevContainer()

    try:
      development_container.container_valid_exception()
      click.echo(_("Detected valid container."))
    except exceptions.DevContainerException:
      click.echo(_("No compatible PIB container found."))
      sys.exit(development_container.incompatible_container_exit_code)
