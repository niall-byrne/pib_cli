"""Tests for External Command Invocations"""

import glob
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from ... import config, patchbay, project_root
from ..internal_commands import execute_internal_command, setup_bash


class TestExecuteInternalCommandFunction(TestCase):

  def setUp(self):
    self.mock_response = "Ready to Test"
    self.test_commands = ["Test Command1", "Test Command2"]

  def validate_calls(self, mock_click, mock_module):
    for command in self.test_commands:
      mock_module.__getitem__.assert_any_call(command)
      mock_click.assert_any_call("Expected Response: " + command)

  @patch(patchbay.INTERNAL_COMMANDS_MODULE)
  @patch(patchbay.CLI_CLICK_ECHO)
  def test_command_call_single(self, mock_click, mock_globals):
    mock_module_dictionary = MagicMock()
    mock_globals.return_value = mock_module_dictionary
    mock_commands = Mock()

    mock_module_dictionary.__getitem__.return_value = mock_commands

    responses = []
    for command in self.test_commands:
      responses.append("Expected Response: " + command)
    mock_commands.side_effect = responses

    execute_internal_command(self.test_commands)
    self.validate_calls(mock_click, mock_module_dictionary)


class TestSetupBash(TestCase):

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_copy_operations(self, mock_exists, mock_copy):
    mock_exists.return_value = True
    setup_bash()
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    for file_name in bash_files:
      mock_copy.assert_any_call(file_name, str(Path.home()))
    self.assertEqual(len(bash_files), mock_copy.call_count)

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_output(self, mock_exists, _):
    mock_exists.return_value = True
    result = setup_bash()
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
    results = setup_bash()
    mock_copy.assert_not_called()
    self.assertEqual(results, config.ERROR_CONTAINER_ONLY)
