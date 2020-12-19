"""Test the CLI"""

from unittest import TestCase
from unittest.mock import Mock, patch

from .. import patchbay
from ..cli import execute_external_command
from .fixtures import CommandTestHarness


class TestExecute(TestCase):

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

  @patch(patchbay.CLI_EXTERNAL_COMMANDS)
  @patch(patchbay.CLI_CLICK_ECHO)
  @patch(patchbay.CLI_SYS_EXIT)
  def test_command_call_single(self, mock_exit, mock_echo, mock_commands):
    self.mock_command_manager.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_command_manager

    execute_external_command(self.test_commands)
    self.validate_calls(None, mock_echo, mock_exit, 0)

  @patch(patchbay.CLI_EXTERNAL_COMMANDS)
  @patch(patchbay.CLI_CLICK_ECHO)
  @patch(patchbay.CLI_SYS_EXIT)
  def test_command_call_with_options(self, mock_exit, mock_echo, mock_commands):
    self.mock_command_manager.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_command_manager
    options = ('one', 'two', 'three')

    execute_external_command(self.test_commands, overload=options)
    self.validate_calls(options, mock_echo, mock_exit, 0)

  @patch(patchbay.CLI_EXTERNAL_COMMANDS)
  @patch(patchbay.CLI_CLICK_ECHO)
  @patch(patchbay.CLI_SYS_EXIT)
  def test_command_call_fails(self, mock_exit, mock_echo, mock_commands):
    mock_commands.return_value = self.mock_command_manager
    options = ('one', 'two', 'three')

    execute_external_command(self.test_commands, overload=options)

    self.mock_invoke.assert_called_once_with(self.test_commands[0], options)
    mock_echo.assert_called_once_with(self.mock_response)
    mock_exit.assert_called_once_with(self.test_exit_code)


class TestBuildDocs(CommandTestHarness):
  __test__ = True
  invocation_command = ['build-docs']
  external_commands = ['build-docs']


class TestBuildWheel(CommandTestHarness):
  __test__ = True
  invocation_command = ['build-wheel']
  external_commands = ['build-wheel']


class TestFormat(CommandTestHarness):
  __test__ = True
  invocation_command = ['fmt']
  external_commands = ['fmt']


class TestLint(CommandTestHarness):
  __test__ = True
  invocation_command = ['lint']
  external_commands = ['lint']


class TestSecTest(CommandTestHarness):
  __test__ = True
  invocation_command = ['sectest']
  external_commands = ['sectest']


class TestUnittests(CommandTestHarness):
  __test__ = True
  invocation_command = ['test']
  external_commands = ['test']
  overload = ()


class TestUnittestsOverload(CommandTestHarness):
  __test__ = True
  invocation_command = ['test']
  external_commands = ['test']
  overload = ('-s',)


class TestCoverage(CommandTestHarness):
  __test__ = True
  invocation_command = ['coverage']
  external_commands = ['coverage']
  overload = ()


class TestCoverageOverload(CommandTestHarness):
  __test__ = True
  invocation_command = ['coverage']
  external_commands = ['coverage']
  overload = ('/specific/file.py',)


class TestReinstallRequirements(CommandTestHarness):
  __test__ = True
  invocation_command = ['reinstall-requirements']
  external_commands = ['reinstall-requirements']


class TestSetupBash(CommandTestHarness):
  __test__ = True
  invocation_command = ['setup-bash']
  python_commands = ['setup-bash']


class TestSetup(CommandTestHarness):
  __test__ = True
  invocation_command = ['setup']
  python_commands = ['setup-bash']
  external_commands = ['reinstall-requirements']
