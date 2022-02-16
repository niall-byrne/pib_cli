"""Tests for the SelectedUserConfigurationEntry class."""

from typing import List, Optional, Union, cast
from unittest import TestCase
from unittest.mock import patch

from pib_cli.config import yaml_keys

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
            "path_method": 'project_docs',
            "command_name": 'test_command',
            "commands": commands if commands else ["default_command"],
            "success": "Successful!",
            "failure": "Failed!",
        }
    )
    if container_only is not None:
      test_data.update({yaml_keys.CONTAINER_ONLY: container_only})
    return test_data

  def create_instance(
      self,
      selected_configuration: yaml_keys.TypeUserConfiguration,
      container: bool = False,
  ) -> selected.SelectedUserConfigurationEntry:
    with patch(
        selected.__name__ + ".dev_container.DevContainer.is_container"
    ) as m_container:
      m_container.return_value = container
      return selected.SelectedUserConfigurationEntry(selected_configuration)

  def test_initialize(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.create_instance(test_data, container=True)

    self.assertTrue(instance.containerized)
    self.assertEqual(instance.user_configuration, test_data)

  def test_initialize_str(self) -> None:
    test_data = self.get_yaml_test_data(
        commands="test_simple_string_command",
        container_only=True,
    )
    instance = self.create_instance(test_data, container=True)

    self.assertTrue(instance.containerized)
    self.assertEqual(instance.user_configuration, test_data)

  def test_inside_container_is_config_executable(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.create_instance(test_data, container=True)

    self.assertTrue(instance.is_executable())

  def test_outside_container_is_config_executable(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.create_instance(test_data, container=False)

    self.assertFalse(instance.is_executable())

  def test_outside_container_is_config_executable_default(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.create_instance(test_data, container=False)

    self.assertTrue(instance.is_executable())

  def test_get_config_path_method(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.create_instance(test_data, container=False)

    self.assertEqual(
        instance.get_config_path_method(),
        test_data['path_method'],
    )

  def test_get_config_commands(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.create_instance(test_data, container=False)

    self.assertEqual(
        instance.get_config_commands(),
        test_data['commands'],
    )

  def test_get_config_response_exit_code_zero(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.create_instance(test_data, container=False)

    self.assertEqual(
        instance.get_config_response(0),
        test_data['success'],
    )

  def test_get_config_response_exit_code_non_zero(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.create_instance(test_data, container=False)

    self.assertEqual(
        instance.get_config_response(99),
        test_data['failure'],
    )
