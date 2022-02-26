"""CommandRunner class."""

import os
from typing import List, Tuple

from pib_cli.support import path_map

from .. import config


class CommandRunner:
  """Runner for configuration based CLI commands.

  :param commands: A list of system calls to be executed
  :param overload: Extra overloaded arguments specified at the CLI
  """

  overload_environment_variable = config.ENV_OVERLOAD_ARGUMENTS

  def __init__(
      self,
      commands: List[str],
      overload: Tuple[str, ...],
      path_map_method: str,
  ) -> None:
    self.commands = commands
    self.exit_code = 127
    self.overload = overload
    self._change_execution_location = getattr(
        path_map.PathMap(),
        path_map_method,
    )

  def execute(self) -> None:
    """Execute the sequence of system calls.

    Execution will terminate immediately if any command fails.
    """

    self._change_execution_location()
    self._insert_overload()
    for command in self.commands:
      self._system_call(command)
      if self.exit_code != 0:
        break
    self._clear_overload()

  def _system_call(self, command: str) -> None:

    result = os.system(command)  # nosec
    self.exit_code = int(result / 256)

  def _insert_overload(self) -> None:

    overload_string = " ".join(self.overload)
    os.environ[self.overload_environment_variable] = overload_string

  def _clear_overload(self) -> None:

    if self.overload_environment_variable in os.environ:
      del os.environ[self.overload_environment_variable]
