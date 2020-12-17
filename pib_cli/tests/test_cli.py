"""Test the CLI"""

from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.cli import execute
from pib_cli.tests.fixtures import CLITestHarness


class TestExecute(TestCase):

  def setUp(self):
    self.mock_response = "Ready to Test"
    self.test_command = "Test Command"
    self.test_exit_code = 99
    self.mock_invoke = Mock()
    self.mock_invoke.return_value = self.mock_response

    self.mock_command_manager = Mock()
    self.mock_command_manager.invoke = self.mock_invoke
    self.mock_command_manager.process_manager.exit_code = self.test_exit_code

  @patch("pib_cli.cli.Commands")
  @patch("pib_cli.cli.click.echo")
  @patch("pib_cli.cli.sys.exit")
  def test_command_call(self, mock_exit, mock_echo, mock_commands):
    mock_commands.return_value = self.mock_command_manager

    execute(self.test_command)

    self.mock_invoke.assert_called_once_with(self.test_command)
    mock_echo.assert_called_once_with(self.mock_response)
    mock_exit.assert_called_once_with(self.test_exit_code)


class TestBuildDocs(CLITestHarness):
  __test__ = True
  invocation_command = ['build-docs']
  internal_command = 'build-docs'


class TestBuildWheel(CLITestHarness):
  __test__ = True
  invocation_command = ['build-wheel']
  internal_command = 'build-wheel'


class TestFormat(CLITestHarness):
  __test__ = True
  invocation_command = ['fmt']
  internal_command = 'fmt'


class TestLint(CLITestHarness):
  __test__ = True
  invocation_command = ['lint']
  internal_command = 'lint'


class TestSecTest(CLITestHarness):
  __test__ = True
  invocation_command = ['sectest']
  internal_command = 'sectest'
