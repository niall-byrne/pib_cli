"""Tests for External Command Invocations."""

from unittest import TestCase
from unittest.mock import Mock, patch

from ... import config, patchbay
from ..configuration import ConfigurationManager
from ..external_commands import ExternalCommands, execute_external_command
from ..path_map import PathMap
from ..processes import ProcessManager
from .fixtures import CommandTestHarness


class TestExecuteExternalCommandFunction(TestCase):
  """Test the execute_external_command function."""

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
  """Test the ExternalCommands class."""

  def setUp(self):
    with patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER, return_value=True):
      self.commands = ExternalCommands()

  def test_initial_instance_variables(self):
    self.assertIsInstance(self.commands.process_manager, ProcessManager)
    self.assertIsInstance(self.commands.path_manager, PathMap)
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
  """Test the build-docs command."""

  __test__ = True
  command = 'build-docs'


class TestBuildWheel(CommandTestHarness):
  """Test the build-wheel command."""

  __test__ = True
  command = 'build-wheel'


class TestFormatter(CommandTestHarness):
  """Test the fmt command."""

  __test__ = True
  command = 'fmt'


class TestLinter(CommandTestHarness):
  """Test the lint command."""

  __test__ = True
  command = 'lint'


class TestSecTest(CommandTestHarness):
  """Test the sectest command."""

  __test__ = True
  command = 'sectest'


class TestTest(CommandTestHarness):
  """Test the test command."""

  __test__ = True
  command = 'test'


class TestTestWithOptions(CommandTestHarness):
  """Test the test command with an overload."""

  __test__ = True
  command = 'test'
  overload = (
      '-x',
      '/specific/file/to/test.py',
  )


class TestCoverage(CommandTestHarness):
  """Test the coverage command."""

  __test__ = True
  command = 'coverage'


class TestCoverageWithOptions(CommandTestHarness):
  """Test the coverage command with an overload."""

  __test__ = True
  command = 'coverage'
  overload = ('/specific/file/to/test.py',)


class TestReinstallRequirements(CommandTestHarness):
  """Test the reinstall-requirements command."""

  __test__ = True
  command = 'reinstall-requirements'
