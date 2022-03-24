"""CommandRunner class."""

import os
from typing import List, Tuple

from pib_cli.support import path_map, state
from typing_extensions import TypedDict

from .. import config


class TypeRunnerEnvVar(TypedDict):
  """Typed representation of a runner's environment variable."""

  name: str
  value: str
  always_set: bool


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
    self._inserted_variable_content: List[str] = []

  def execute(self) -> None:
    """Execute the sequence of system calls.

    Execution will terminate immediately if any command fails.
    """

    self._change_execution_location()
    self._setup_environment()
    for command in self.commands:
      self._system_call(command)
      if self.exit_code != 0:
        break
    self._clear_environment()

  def _system_call(self, command: str) -> None:

    result = os.system(command)  # nosec
    self.exit_code = int(result / 256)

  def _clear_environment(self) -> None:

    for env_var in self._inserted_variable_content:
      del os.environ[env_var]

  def _setup_environment(self) -> None:
    for env in self._get_environment_config():
      if env['name'] not in os.environ or env['always_set']:
        os.environ[env['name']] = env['value']
        self._inserted_variable_content.append(env['name'])

  def _get_environment_config(self) -> List[TypeRunnerEnvVar]:
    user_configuration = state.State().user_config
    return [
        TypeRunnerEnvVar(
            name=config.ENV_OVERRIDE_PROJECT_NAME,
            value=user_configuration.get_project_name(),
            always_set=False,
        ),
        TypeRunnerEnvVar(
            name=config.ENV_OVERRIDE_DOCUMENTATION_ROOT,
            value=user_configuration.get_documentation_root(),
            always_set=False,
        ),
        TypeRunnerEnvVar(
            name=self.overload_environment_variable,
            value=" ".join(self.overload),
            always_set=True,
        ),
    ]
