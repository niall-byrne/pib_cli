"""Tests for the CommandSelector class."""

from typing import Type, cast

from pib_cli.config import yaml_keys
from pib_cli.support.user_configuration.bases.fixtures import (
    command_selector_base_harness,
)

from .. import command_selector_legacy


class TestCommandSelector(
    command_selector_base_harness.CommandSelectorBaseTestHarness
):
  """Tests for the CommandSelector class."""

  test_class: Type[command_selector_legacy.LegacyCommandSelector]
  test_data = {
      yaml_keys.COMMAND_NAME: 'test_command',
      yaml_keys.COMMAND_DESCRIPTION: "A test command",
      yaml_keys.LEGACY_PATH_METHOD: 'project_docs',
      yaml_keys.SUCCESS: "Successful!",
      yaml_keys.FAILURE: "Failed!",
  }

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_selector_legacy.LegacyCommandSelector

  def test_get_config_path_method(self) -> None:
    test_data = cast(
        yaml_keys.TypeLegacyUserConfiguration,
        self.get_yaml_test_data(),
    )
    instance = self.test_class(test_data)

    for path_method in ["project_docs", "project_root", "project_home"]:
      test_data[yaml_keys.LEGACY_PATH_METHOD] = path_method
      self.assertEqual(
          instance.get_config_path_method(),
          instance.legacy_path_method_mapping[path_method],
      )
