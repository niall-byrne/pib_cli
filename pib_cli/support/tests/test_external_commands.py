"""Tests for External Command Invocations"""

from unittest import TestCase
from unittest.mock import Mock, patch

from ... import config, patchbay
from ...config import yaml_keys
from ..configuration import ConfigurationManager
from ..external_commands import ExternalCommands, execute_external_command
from ..paths import ContainerPathManager
from ..processes import ProcessManager
from .fixtures import CommandTestHarness


class TestExecuteExternalCommandFunction(TestCase):

  def setUp(self):
    self.mock_response = "Ready to Test"
    self.test_commands = ["Test Command1", "Test Command2"]
    self.test_exit_code = 99
    self.mock_invoke = Mock()
    self.mock_invoke.return_value = self.mock_response

    self.mock_command_manager = Mock()
    self.mock_command_manager.invoke = self.mock_invoke
    self.mock_command_manager.process_manager.exit_code = self.test_exit_code

  def validate_calls(self, options, mock_echo, mock_exit, exit_code):
    for command in self.test_commands:
      self.mock_invoke.assert_any_call(command, options)
      mock_echo.assert_any_call(self.mock_response)
    mock_exit.assert_called_once_with(exit_code)

    self.assertEqual(len(self.test_commands), self.mock_invoke.call_count)
    self.assertEqual(len(self.test_commands), mock_echo.call_count)

  @patch(patchbay.EXTERNAL_COMMANDS)
  @patch(patchbay.CLI_CLICK_ECHO)
  @patch(patchbay.EXTERNAL_COMMANDS_SYS_EXIT)
  def test_command_call_single(self, mock_exit, mock_echo, mock_commands):
    self.mock_command_manager.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_command_manager

    execute_external_command(self.test_commands)
    self.validate_calls(None, mock_echo, mock_exit, 0)

  @patch(patchbay.EXTERNAL_COMMANDS)
  @patch(patchbay.CLI_CLICK_ECHO)
  @patch(patchbay.EXTERNAL_COMMANDS_SYS_EXIT)
  def test_command_call_with_options(self, mock_exit, mock_echo, mock_commands):
    self.mock_command_manager.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_command_manager
    options = ('one', 'two', 'three')

    execute_external_command(self.test_commands, overload=options)
    self.validate_calls(options, mock_echo, mock_exit, 0)

  @patch(patchbay.EXTERNAL_COMMANDS)
  @patch(patchbay.CLI_CLICK_ECHO)
  @patch(patchbay.EXTERNAL_COMMANDS_SYS_EXIT)
  def test_command_call_fails(self, mock_exit, mock_echo, mock_commands):
    mock_commands.return_value = self.mock_command_manager
    options = ('one', 'two', 'three')

    execute_external_command(self.test_commands, overload=options)

    self.mock_invoke.assert_called_once_with(self.test_commands[0], options)
    mock_echo.assert_called_once_with(self.mock_response)
    mock_exit.assert_called_once_with(self.test_exit_code)


class TestCommandClass(TestCase):

  def yaml_test_data(self, path_method, test_command, container_only):
    return {
        yaml_keys.COMMAND_NAME: test_command,
        yaml_keys.CONTAINER_ONLY: container_only,
        yaml_keys.PATH_METHOD: path_method,
        yaml_keys.COMMANDS: "Some Command"
    }

  def setUp(self):
    with patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER, return_value=True):
      self.commands = ExternalCommands()

  def test_initial_instance_variables(self):
    self.assertIsInstance(self.commands.process_manager, ProcessManager)
    self.assertIsInstance(self.commands.path_manager, ContainerPathManager)
    self.assertIsInstance(
        self.commands.configuration_manager, ConfigurationManager
    )

  def test_invoke_non_existent_command(self):
    with self.assertRaises(KeyError):
      self.commands.invoke("non-existent-command", None)

  def test_invoke_non_existent_command_with_options(self):
    with self.assertRaises(KeyError):
      self.commands.invoke("non-existent-command", ('option1',))

  @patch(patchbay.CONFIGURATION_MANAGER_IS_CONFIG_EXECUTABLE)
  @patch(patchbay.CONFIGURATION_MANAGER_FIND_CONFIG)
  def test_outside_container_flag_fails(self, mock_config, mock_exec):
    mock_config.return_value = None
    mock_exec.return_value = False

    response = self.commands.invoke("test_command", None)
    self.assertEqual(response, config.ERROR_CONTAINER_ONLY)
    self.assertEqual(0, self.commands.process_manager.exit_code)

  @patch(patchbay.CONFIGURATION_MANAGER_IS_CONFIG_EXECUTABLE)
  @patch(patchbay.CONFIGURATION_MANAGER_FIND_CONFIG)
  @patch(patchbay.CONFIGURATION_MANAGER_GET_CONFIG_PATH_METHOD)
  def test_outside_container_flag_succeeds(
      self,
      mock_path,
      mock_config,
      mock_exec,
  ):
    expected_exception = "Expected Exception!"
    mock_config.return_value = None
    mock_exec.return_value = True
    mock_path.side_effect = Exception(expected_exception)

    with self.assertRaises(Exception) as raised_error:
      self.commands.invoke("test_command", None)
    self.assertEqual(
        raised_error.exception.args[0],
        expected_exception,
    )


class TestBuildDocs(CommandTestHarness):
  __test__ = True
  command = 'build-docs'


class TestBuildWheel(CommandTestHarness):
  __test__ = True
  command = 'build-wheel'


class TestFormatter(CommandTestHarness):
  __test__ = True
  command = 'fmt'


class TestLinter(CommandTestHarness):
  __test__ = True
  command = 'lint'


class TestSecTest(CommandTestHarness):
  __test__ = True
  command = 'sectest'


class TestTest(CommandTestHarness):
  __test__ = True
  command = 'test'


class TestTestWithOptions(CommandTestHarness):
  __test__ = True
  command = 'test'
  overload = (
      '-x',
      '/specific/file/to/test.py',
  )


class TestCoverage(CommandTestHarness):
  __test__ = True
  command = 'coverage'


class TestCoverageWithOptions(CommandTestHarness):
  __test__ = True
  command = 'coverage'
  overload = ('/specific/file/to/test.py',)


class TestReinstallRequirements(CommandTestHarness):
  __test__ = True
  command = 'reinstall-requirements'
