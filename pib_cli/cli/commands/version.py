"""VersionCommand class."""

import click
import pkg_resources

from .bases import command


class VersionCommand(command.CommandBase):
  """CLI command to report the PIB CLI version."""

  def invoke(self) -> None:
    """Invoke the command."""

    click.echo(
        "pib_cli version: "
        f"{pkg_resources.get_distribution('pib_cli').version}",
    )
