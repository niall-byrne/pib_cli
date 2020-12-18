"""Test the CLI"""

from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.cli import execute
from pib_cli.tests.fixtures import CLITestHarness


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

  @patch("pib_cli.cli.Commands")
  @patch("pib_cli.cli.click.echo")
  @patch("pib_cli.cli.sys.exit")
  def test_command_call_single(self, mock_exit, mock_echo, mock_commands):
    self.mock_command_manager.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_command_manager

    execute(self.test_commands)
    self.validate_calls(None, mock_echo, mock_exit, 0)

  @patch("pib_cli.cli.Commands")
  @patch("pib_cli.cli.click.echo")
  @patch("pib_cli.cli.sys.exit")
  def test_command_call_with_options(self, mock_exit, mock_echo, mock_commands):
    self.mock_command_manager.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_command_manager
    options = ('one', 'two', 'three')

    execute(self.test_commands, overload=options)
    self.validate_calls(options, mock_echo, mock_exit, 0)

  @patch("pib_cli.cli.Commands")
  @patch("pib_cli.cli.click.echo")
  @patch("pib_cli.cli.sys.exit")
  def test_command_call_fails(self, mock_exit, mock_echo, mock_commands):
    mock_commands.return_value = self.mock_command_manager
    options = ('one', 'two', 'three')

    execute(self.test_commands, overload=options)

    self.mock_invoke.assert_called_once_with(self.test_commands[0], options)
    mock_echo.assert_called_once_with(self.mock_response)
    mock_exit.assert_called_once_with(self.test_exit_code)


class TestBuildDocs(CLITestHarness):
  __test__ = True
  invocation_command = ['build-docs']
  internal_commands = ['build-docs']


class TestBuildWheel(CLITestHarness):
  __test__ = True
  invocation_command = ['build-wheel']
  internal_commands = ['build-wheel']


class TestFormat(CLITestHarness):
  __test__ = True
  invocation_command = ['fmt']
  internal_commands = ['fmt']


class TestLint(CLITestHarness):
  __test__ = True
  invocation_command = ['lint']
  internal_commands = ['lint']


class TestSecTest(CLITestHarness):
  __test__ = True
  invocation_command = ['sectest']
  internal_commands = ['sectest']


class TestUnittests(CLITestHarness):
  __test__ = True
  invocation_command = ['test']
  internal_commands = ['test']
  overload = ()


class TestUnittestsOverload(CLITestHarness):
  __test__ = True
  invocation_command = ['test']
  internal_commands = ['test']
  overload = ('-s',)


class TestCoverage(CLITestHarness):
  __test__ = True
  invocation_command = ['coverage']
  internal_commands = ['coverage']
  overload = ()


class TestCoverageOverload(CLITestHarness):
  __test__ = True
  invocation_command = ['coverage']
  internal_commands = ['coverage']
  overload = ('/specific/file.py',)


class TestReinstallRequirements(CLITestHarness):
  __test__ = True
  invocation_command = ['reinstall-requirements']
  internal_commands = ['reinstall-requirements']


class TestSetupBash(CLITestHarness):
  __test__ = True
  invocation_command = ['setup-bash']
  internal_commands = ['setup-bash']


class TestSetup(CLITestHarness):
  __test__ = True
  invocation_command = ['setup']
  internal_commands = ['setup-bash', 'reinstall-requirements']
