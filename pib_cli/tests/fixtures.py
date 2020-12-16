"""Test Fixtures"""

from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from pib_cli.commander import cli


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
  expected_system_call = None
  success_message = None
  failure_message = None
  command_path_method = None

  def setUp(self):
    self.runner = CliRunner()
    self.mock_utils = MockUtilities()
    self.invocation_command = self.__class__.invocation_command
    self.expected_system_call = self.__class__.expected_system_call
    self.success_message = self.__class__.success_message
    self.failure_message = self.__class__.failure_message
    self.command_path_method = self.__class__.command_path_method

  @patch("pib_cli.commander.Utilities")
  def test_command_executed_in_correct_path(self, mock_utils):
    self.mock_utils.process_manager.exit_code = 0
    mock_utils.return_value = self.mock_utils
    method = getattr(self.mock_utils.path_manager, self.command_path_method)
    self.runner.invoke(cli, self.invocation_command)
    method.assert_called_once_with()

  @patch("pib_cli.commander.Utilities")
  def test_build_docs_successful(self, mock_utils):
    self.mock_utils.process_manager.exit_code = 0
    mock_utils.return_value = self.mock_utils

    result = self.runner.invoke(cli, self.invocation_command)
    self.mock_utils.process_manager.spawn.assert_called_once_with(
        self.expected_system_call)
    self.assertEqual(result.exit_code,
                     self.mock_utils.process_manager.exit_code)
    self.assertEqual(result.output, '%s\n' % self.success_message)

  @patch("pib_cli.commander.Utilities")
  def test_build_docs_unsuccessful(self, mock_utils):
    self.mock_utils.process_manager.exit_code = 1
    mock_utils.return_value = self.mock_utils

    result = self.runner.invoke(cli, self.invocation_command)

    self.mock_utils.process_manager.spawn.assert_called_once_with(
        self.expected_system_call)
    self.assertEqual(result.exit_code,
                     self.mock_utils.process_manager.exit_code)
    self.assertEqual(result.output, '%s\n' % self.failure_message)
