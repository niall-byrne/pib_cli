"""Built in CLI container commands."""

import click
from pib_cli.cli.commands import (
    container_setup,
    container_validate,
    container_version,
    handler,
)
from pib_cli.config.locale import _


@click.group(_("container"))
def container() -> None:
  """PIB container commands."""


@container.command(_("setup"))
def setup_container_builtin() -> None:
  """Copy file assets to setup the development container."""

  handler(container_setup.ContainerSetupCommand)

@container.command(_("validate"))
def validate_container_builtin() -> None:
  """Validate the current container is compatible with the CLI."""

  handler(container_validate.ContainerValidateCommand)

@container.command(_("version"))
def version_container_builtin() -> None:
  """Display the current container version."""

  handler(container_version.ContainerVersionCommand)


container_commands: click.Command = container
