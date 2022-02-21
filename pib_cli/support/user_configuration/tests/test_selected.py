"""Tests for the SelectedUserConfigurationEntry class."""

from typing import List, Optional, Union, cast
from unittest import TestCase
from unittest.mock import patch

from pib_cli.config import yaml_keys
from pib_cli.support import container
from pib_cli.support.container import exceptions

from .. import selected


class TestSelectedUserConfigurationEntry(TestCase):
  """Tests for the SelectedUserConfigurationEntry class."""

  def get_yaml_test_data(
      self,
      commands: Optional[Union[str, List[str]]] = None,
      container_only: Optional[bool] = None,
  ) -> yaml_keys.TypeUserConfiguration:
    test_data = cast(
        yaml_keys.TypeUserConfiguration, {
            "path": 'documentation_root',
            "command_name": 'test_command',
            "commands": commands if commands else ["default_command"],
            "success": "Successful!",
            "failure": "Failed!",
        }
    )
    if container_only is not None:
      test_data.update({yaml_keys.CONTAINER_ONLY: container_only})
    return test_data

  def create_patched_instance(
      self,
      selected_configuration: yaml_keys.TypeUserConfiguration,
      valid_container: bool,
  ) -> selected.SelectedUserConfigurationEntry:
    with patch(selected.__name__ + ".container.DevContainer") as m_container:
      if not valid_container:
        valid = m_container.return_value.container_valid_exception
        valid.side_effect = exceptions.DevContainerException
      return selected.SelectedUserConfigurationEntry(selected_configuration)

  def test_initialize(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = selected.SelectedUserConfigurationEntry(test_data)

    self.assertIsInstance(instance.container, container.DevContainer)
    self.assertEqual(instance.user_configuration, test_data)

  def test_initialize_str(self) -> None:
    test_data = self.get_yaml_test_data(
        commands="test_simple_string_command",
        container_only=True,
    )
    instance = selected.SelectedUserConfigurationEntry(test_data)

    self.assertIsInstance(instance.container, container.DevContainer)
    self.assertEqual(instance.user_configuration, test_data)

  def test_inside_container_is_config_executable(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.create_patched_instance(test_data, valid_container=True)

    self.assertTrue(instance.is_executable())

  def test_outside_container_is_config_executable(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.create_patched_instance(test_data, valid_container=False)

    self.assertFalse(instance.is_executable())

  def test_outside_container_is_config_executable_default(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.create_patched_instance(test_data, valid_container=False)

    self.assertTrue(instance.is_executable())

  def test_get_config_path_method(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = selected.SelectedUserConfigurationEntry(test_data)

    self.assertEqual(
        instance.get_config_path_method(),
        test_data['path'],
    )

  def test_get_config_commands(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = selected.SelectedUserConfigurationEntry(test_data)

    self.assertEqual(
        instance.get_config_commands(),
        test_data['commands'],
    )

  def test_get_config_response_exit_code_zero(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = selected.SelectedUserConfigurationEntry(test_data)

    self.assertEqual(
        instance.get_config_response(0),
        test_data['success'],
    )

  def test_get_config_response_exit_code_non_zero(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = selected.SelectedUserConfigurationEntry(test_data)

    self.assertEqual(
        instance.get_config_response(99),
        test_data['failure'],
    )
