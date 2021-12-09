"""Tests for Internal Commands."""

import glob
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import pkg_resources

from ... import config, patchbay, project_root
from ..internal_commands import InternalCommands, execute_internal_command
from ..paths import DevContainerPathManager
from ..processes import ProcessManager


class TestExecuteInternalCommandFunction(TestCase):
  """Test the execute_internal_command function."""

  def setUp(self):
    self.mock_response = "Ready to Test"
    self.test_commands = ["Test_Command1", "Test_Command2"]

  def validate_calls(self, mock_click, mock_commands):
    for command in self.test_commands:
      mock_command = getattr(mock_commands.return_value, command)
      mock_command.assert_called_once_with()
      mock_click.assert_any_call("Expected Response: " + command)

  @patch(patchbay.INTERNAL_COMMANDS_CLASS)
  @patch(patchbay.CLI_CLICK_ECHO)
  def test_command_call_single(self, mock_click, mock_commands):

    mock_internal_command_class = Mock()

    for command in self.test_commands:
      command_mock = Mock()
      command_mock.return_value = "Expected Response: " + command
      setattr(mock_internal_command_class, command, command_mock)

    mock_commands.return_value = mock_internal_command_class
    execute_internal_command(self.test_commands)
    self.validate_calls(mock_click, mock_commands)


class TestInternalCommands(TestCase):
  """Test the InternalCommands class."""

  def setUp(self):
    with patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER, return_value=True):
      self.internal_commands = InternalCommands()

  def test_initial_instance_variables(self):
    self.assertIsInstance(
        self.internal_commands.process_manager, ProcessManager
    )
    self.assertIsInstance(
        self.internal_commands.path_manager, DevContainerPathManager
    )

  @patch(patchbay.INTERNAL_COMMANDS_GET_CONFIG_FILE_NAME)
  def test_config_location(self, mock_config_file):
    mock_config_file.return_value = "/mock/path"
    result = self.internal_commands.config_location()
    self.assertEqual(
        result,
        f"Current Configuration: {mock_config_file.return_value}",
    )

  @patch(patchbay.INTERNAL_COMMANDS_GET_CONFIG_FILE_NAME)
  def test_config_show(self, mock_config_file):
    mock_config_file.return_value = "/mock/path"
    mock_configuration = "mock config data "

    with patch(
        "builtins.open",
        mock_open(read_data=mock_configuration),
    ) as mock_config_data:
      result = self.internal_commands.config_show()
      mock_config_data.assert_called_once_with(
          mock_config_file.return_value,
          encoding='utf-8',
      )
      self.assertEqual(result, mock_configuration.strip())

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  @patch(patchbay.INTERNAL_COMMANDS_MAKE_DIRS)
  def test_setup_bash_copy_operations(self, _, mock_exists, mock_copy):
    mock_exists.return_value = True
    self.internal_commands.setup_bash()
    bash_files = glob.glob(os.path.join(project_root, "bash", "bash*"))
    home_dir = str(Path.home())
    for file_name in bash_files:
      dotted_name = "." + os.path.basename(file_name)
      mock_copy.assert_any_call(file_name, os.path.join(home_dir, dotted_name))
    self.assertEqual(len(bash_files) + 1, mock_copy.call_count)

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  @patch(patchbay.INTERNAL_COMMANDS_MAKE_DIRS)
  def test_setup_bash_shim_copy(self, mock_dirs, mock_exists, mock_copy):
    mock_exists.return_value = True
    self.internal_commands.setup_bash()
    shim_file = os.path.join(project_root, "bash", "shim")
    destination = os.path.join(config.LOCAL_EXECUTABLES, "dev")
    mock_copy.assert_any_call(shim_file, destination)
    mock_dirs.assert_called_once_with(config.LOCAL_EXECUTABLES, exist_ok=True)

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  @patch(patchbay.INTERNAL_COMMANDS_MAKE_DIRS)
  def test_setup_bash_output(self, _, mock_exists, __):
    mock_exists.return_value = True
    result = self.internal_commands.setup_bash()
    home_dir = str(Path.home())
    expected_results = []

    bash_files = glob.glob(os.path.join(project_root, "bash", "bash*"))
    for file_name in bash_files:
      dotted_name = "." + os.path.basename(file_name)
      destination = os.path.join(home_dir, dotted_name)
      expected_results.append(f"Copied: {file_name} -> {destination} ")

    shim_file = os.path.join(project_root, "bash", "shim")
    destination = os.path.join(config.LOCAL_EXECUTABLES, "dev")
    expected_results.append(f"Copied: {shim_file} -> {destination} ")

    expected_results.append(config.SETTING_BASH_SETUP_SUCCESS_MESSAGE)
    self.assertEqual(result, "\n".join(expected_results))

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_outside_container(self, mock_exists, mock_copy):
    mock_exists.return_value = False
    results = self.internal_commands.setup_bash()
    mock_copy.assert_not_called()
    self.assertEqual(results, config.ERROR_CONTAINER_ONLY)

  def test_version(self):
    results = self.internal_commands.version()
    self.assertEqual(
        results,
        (
            "pib_cli version: "
            f"{pkg_resources.get_distribution('pib_cli').version}"
        ),
    )
