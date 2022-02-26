"""CustomizedCommand class."""

import sys
from typing import Tuple

import click
from pib_cli.support import runner
from pib_cli.support.container import exceptions
from pib_cli.support.user_configuration.selected import (
    SelectedUserConfigurationEntry,
)

from .bases import command


class CustomizedCommand(command.CommandBase):
  """CLI command to execute a configuration defined command.

  :param command_configuration: The configured command's Python representation.
  :param overload: Additional parameters passed to the CLI interface.
  """

  container_only_error_exit_code = 127

  def __init__(
      self,
      command_configuration: SelectedUserConfigurationEntry,
      overload: Tuple[str, ...],
  ) -> None:
    self.command_configuration = command_configuration
    self.overload = overload

  def invoke(self) -> None:
    """Invoke the command."""

    try:
      self.command_configuration.is_executable_exception()
      self._call_runner()
    except exceptions.DevContainerException as exc:
      click.echo("ERROR: {container_error}".format(container_error=exc.args[0]))
      sys.exit(self.container_only_error_exit_code)

  def _call_runner(self) -> None:
    command_runner = runner.CommandRunner(
        commands=self.command_configuration.get_config_commands(),
        path_map_method=self.command_configuration.get_config_path_method(),
        overload=self.overload
    )

    command_runner.execute()

    click.echo(
        self.command_configuration.get_config_response(
            command_runner.exit_code
        )
    )

    sys.exit(command_runner.exit_code)
