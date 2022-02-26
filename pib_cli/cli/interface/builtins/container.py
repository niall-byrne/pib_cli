"""Built in CLI container commands."""

import click
from pib_cli.cli.commands import container_setup, container_version, handler


@click.group("container")
def container() -> None:
  """PIB container commands."""


@container.command("setup")
def setup_container_builtin() -> None:
  """Copy file assets to setup the development container."""

  handler(container_setup.ContainerSetupCommand)


@container.command("version")
def version_container_builtin() -> None:
  """Display the current container version."""

  handler(container_version.ContainerVersionCommand)


container_commands: click.Command = container
