"""Tests for External Command Invocations"""

import glob
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from ... import config, patchbay, project_root
from ..internal_commands import InternalCommands, execute_internal_command
from ..paths import ContainerPathManager
from ..processes import ProcessManager


class TestExecuteInternalCommandFunction(TestCase):

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

  def setUp(self):
    with patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER, return_value=True):
      self.internal_commands = InternalCommands()

  def test_initial_instance_variables(self):
    self.assertIsInstance(
        self.internal_commands.process_manager, ProcessManager
    )
    self.assertIsInstance(
        self.internal_commands.path_manager, ContainerPathManager
    )

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_copy_operations(self, mock_exists, mock_copy):
    mock_exists.return_value = True
    self.internal_commands.setup_bash()
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    for file_name in bash_files:
      mock_copy.assert_any_call(file_name, str(Path.home()))
    self.assertEqual(len(bash_files), mock_copy.call_count)

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_output(self, mock_exists, _):
    mock_exists.return_value = True
    result = self.internal_commands.setup_bash()
    home_dir = str(Path.home())
    expected_results = []
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    for file_name in bash_files:
      expected_results.append(f"Copied: {file_name} -> {home_dir} ")
    expected_results.append(config.SETTING_BASH_SETUP_SUCCESS_MESSAGE)
    self.assertEqual(result, "\n".join(expected_results))

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_outside_container(self, mock_exists, mock_copy):
    mock_exists.return_value = False
    results = self.internal_commands.setup_bash()
    mock_copy.assert_not_called()
    self.assertEqual(results, config.ERROR_CONTAINER_ONLY)
