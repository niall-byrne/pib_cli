"""PyTest configuration file."""

# pylint: disable=redefined-outer-name

from typing import Callable, Tuple

import pytest
from pib_cli.config import yaml_keys

from .. import runner

CommandRunnerCreatorType = Callable[[Tuple[str, ...]], runner.CommandRunner]


@pytest.fixture
def mock_configuration() -> yaml_keys.TypeUserConfiguration:

  return {
      yaml_keys.PATH_METHOD: 'documentation_root',
      yaml_keys.COMMAND_NAME: 'test_command',
      yaml_keys.COMMAND_DESCRIPTION: "The test command",
      yaml_keys.COMMANDS:
          [
              "/bin/test_command_step_1",
              "/bin/test_command_step_2",
              "/bin/test_command_step_3",
          ],
      yaml_keys.SUCCESS: "Successful!",
      yaml_keys.FAILURE: "Failed!",
  }


@pytest.fixture
def command_runner_creator(
    mock_configuration: yaml_keys.TypeUserConfiguration
) -> CommandRunnerCreatorType:

  def create_command_runner(overload: Tuple[str, ...]) -> runner.CommandRunner:
    return runner.CommandRunner(
        commands=mock_configuration[yaml_keys.COMMANDS],
        overload=overload,
        path_map_method=mock_configuration[yaml_keys.PATH_METHOD],
    )

  return create_command_runner
