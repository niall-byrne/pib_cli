"""Tests for Configuration Manager"""

from unittest import TestCase
from unittest.mock import patch

import yaml

from ... import config_filename, patchbay
from ...config import yaml_keys
from ..configuration import ConfigurationManager


class TestConfigurationManager(TestCase):

  def yaml_test_data(self, path_method, command_name, commands, container_only):
    self.configuration_manager.config.append(
        {
            yaml_keys.COMMAND_NAME: command_name,
            yaml_keys.CONTAINER_ONLY: container_only,
            yaml_keys.PATH_METHOD: path_method,
            yaml_keys.COMMANDS: commands,
        }
    )

  def setUp(self):
    self.configuration_manager = ConfigurationManager()
    with open(config_filename) as file_handle:
      self.config = yaml.safe_load(file_handle)

  def test_initial_instance_variables(self):
    self.assertListEqual(self.config, self.configuration_manager.config)

  def test_find_config_entry_non_existent_command(self):
    with self.assertRaises(KeyError):
      self.configuration_manager.find_config_entry("non-existent-command")

  def test_find_config_entry(self):
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = ["Some Command"]
    self.yaml_test_data(path_method, command_name, commands, True)

    self.configuration_manager.find_config_entry(command_name)
    self.assertEqual(
        self.configuration_manager.config_entry[yaml_keys.PATH_METHOD],
        path_method,
    )
    self.assertEqual(
        self.configuration_manager.config_entry[yaml_keys.COMMAND_NAME],
        command_name,
    )
    self.assertEqual(
        self.configuration_manager.config_entry[yaml_keys.COMMANDS],
        commands,
    )
    self.assertTrue(
        self.configuration_manager.config_entry[yaml_keys.CONTAINER_ONLY],
    )

  def test_find_config_entry_coerced_from_string(self):
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = "Some Command"
    self.yaml_test_data(path_method, command_name, commands, True)

    self.configuration_manager.find_config_entry(command_name)
    self.assertEqual(
        self.configuration_manager.config_entry[yaml_keys.PATH_METHOD],
        path_method,
    )
    self.assertEqual(
        self.configuration_manager.config_entry[yaml_keys.COMMAND_NAME],
        command_name,
    )
    self.assertEqual(
        self.configuration_manager.config_entry[yaml_keys.COMMANDS],
        [commands],
    )
    self.assertTrue(
        self.configuration_manager.config_entry[yaml_keys.CONTAINER_ONLY],
    )

  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER)
  def test_inside_container_is_config_executable(self, mock_container):
    mock_container.return_value = True
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = ["Some Commands"]
    container_only = True
    self.yaml_test_data(path_method, command_name, commands, container_only)

    self.configuration_manager.find_config_entry(command_name)
    self.assertTrue(self.configuration_manager.is_config_executable())

  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER)
  def test_outside_container_is_config_executable_false(self, mock_container):
    mock_container.return_value = False
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = ["Some Commands"]
    container_only = True
    self.yaml_test_data(path_method, command_name, commands, container_only)

    self.configuration_manager.find_config_entry(command_name)
    self.assertFalse(self.configuration_manager.is_config_executable())

  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER)
  def test_outside_container_is_config_executable_true(self, mock_container):
    mock_container.return_value = False
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = ["Some Commands"]
    container_only = False
    self.yaml_test_data(path_method, command_name, commands, container_only)

    self.configuration_manager.find_config_entry(command_name)
    self.assertTrue(self.configuration_manager.is_config_executable())

  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER)
  def test_is_config_executable_missing_true(self, mock_container):
    mock_container.return_value = False
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = ["Some Commands"]
    self.configuration_manager.config.append(
        {
            yaml_keys.COMMAND_NAME: command_name,
            yaml_keys.PATH_METHOD: path_method,
            yaml_keys.COMMANDS: commands,
        }
    )

    self.configuration_manager.find_config_entry(command_name)
    self.assertTrue(self.configuration_manager.is_config_executable())

  def test_get_config_path_method(self):
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = "Some Command"
    self.yaml_test_data(path_method, command_name, commands, True)
    self.configuration_manager.find_config_entry(command_name)
    self.assertEqual(
        self.configuration_manager.get_config_path_method(),
        path_method,
    )

  def test_get_config_commands(self):
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = "Some Command"
    self.yaml_test_data(path_method, command_name, commands, True)
    self.configuration_manager.find_config_entry(command_name)
    self.assertEqual(
        self.configuration_manager.get_config_commands(),
        [commands],
    )

  def test_get_config_response_exit_code_zero(self):
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = "Some Command"
    success = "Successful"
    self.configuration_manager.config.append(
        {
            yaml_keys.COMMAND_NAME: command_name,
            yaml_keys.PATH_METHOD: path_method,
            yaml_keys.COMMANDS: commands,
            yaml_keys.SUCCESS: success
        }
    )

    self.configuration_manager.find_config_entry(command_name)
    self.assertEqual(
        self.configuration_manager.get_config_response(0),
        success,
    )

  def test_get_config_response_exit_code_non_zero(self):
    path_method = 'non_existent'
    command_name = 'test_command'
    commands = "Some Command"
    failure = "Unsuccessful"
    self.configuration_manager.config.append(
        {
            yaml_keys.COMMAND_NAME: command_name,
            yaml_keys.PATH_METHOD: path_method,
            yaml_keys.COMMANDS: commands,
            yaml_keys.FAILURE: failure
        }
    )

    self.configuration_manager.find_config_entry(command_name)
    self.assertEqual(
        self.configuration_manager.get_config_response(99),
        failure,
    )
