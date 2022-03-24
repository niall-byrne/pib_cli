"""Tests for the CommandSelector class."""

from typing import Type, cast

from pib_cli.config import yaml_keys
from pib_cli.support.user_configuration.bases.fixtures import (
    command_selector_base_harness,
)

from .. import command_selector


class TestCommandSelector(
    command_selector_base_harness.CommandSelectorBaseTestHarness
):
  """Tests for the CommandSelector class."""

  test_class: Type[command_selector.CommandSelector]
  test_data = {
      yaml_keys.COMMAND_NAME: 'test_command',
      yaml_keys.COMMAND_DESCRIPTION: "A test command",
      yaml_keys.PATH_METHOD: 'documentation_root',
      yaml_keys.SUCCESS: "Successful!",
      yaml_keys.FAILURE: "Failed!",
  }

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_selector.CommandSelector

  def test_get_config_path_method(self) -> None:
    test_data = cast(
        yaml_keys.TypeUserConfiguration,
        self.get_yaml_test_data(),
    )
    instance = self.test_class(test_data)

    for path_method in ["documentation_root", "repo_root", "project_root"]:
      test_data[yaml_keys.PATH_METHOD] = path_method
      self.assertEqual(
          instance.get_config_path_method(),
          path_method,
      )
