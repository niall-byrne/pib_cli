"""Test Fixtures"""

from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from pib_cli.cli import cli


class MockUtilities:

  def __init__(self):
    self.process_manager = Mock()
    self.process_manager.spawn = Mock()
    self.process_manager.exit_code = 0
    self.path_manager = Mock()
    self.path_manager.project_root = Mock()


class CommandTestHarness(TestCase):
  __test__ = False

  invocation_command = None
  expected_system_calls = None
  success_message = None
  failure_message = None
  command_path_method = None

  def setUp(self):
    self.runner = CliRunner()
    self.mock_commands = MockUtilities()
    self.invocation_command = self.__class__.invocation_command
    self.expected_system_calls = self.__class__.expected_system_calls
    self.success_message = self.__class__.success_message
    self.failure_message = self.__class__.failure_message
    self.command_path_method = self.__class__.command_path_method

  @patch("pib_cli.cli.Commands")
  def test_command_executed_in_correct_path(self, mock_commands):
    self.mock_commands.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_commands
    method = getattr(self.mock_commands.path_manager, self.command_path_method)
    self.runner.invoke(cli, self.invocation_command)
    method.assert_called_once_with()

  @patch("pib_cli.cli.Commands")
  def test_successful_system_calls(self, mock_commands):
    self.mock_commands.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_commands

    self.runner.invoke(cli, self.invocation_command)
    self.mock_commands.process_manager.spawn.assert_called_once_with(
        self.expected_system_calls)

  @patch("pib_cli.cli.Commands")
  def test_successful_results(self, mock_commands):
    self.mock_commands.process_manager.exit_code = 0
    mock_commands.return_value = self.mock_commands

    result = self.runner.invoke(cli, self.invocation_command)
    self.assertEqual(result.exit_code,
                     self.mock_commands.process_manager.exit_code)
    self.assertEqual(result.output, '%s\n' % self.success_message)

  @patch("pib_cli.cli.Commands")
  def test_unsuccessful_system_calls_only_first(self, mock_commands):
    self.mock_commands.process_manager.exit_code = 1
    mock_commands.return_value = self.mock_commands

    self.runner.invoke(cli, self.invocation_command)
    self.mock_commands.process_manager.spawn.assert_called_once_with(
        self.expected_system_calls)

  @patch("pib_cli.cli.Commands")
  def test_unsuccessful_results(self, mock_commands):
    self.mock_commands.process_manager.exit_code = 1
    mock_commands.return_value = self.mock_commands

    result = self.runner.invoke(cli, self.invocation_command)
    self.assertEqual(result.exit_code,
                     self.mock_commands.process_manager.exit_code)
    self.assertEqual(result.output, '%s\n' % self.failure_message)
