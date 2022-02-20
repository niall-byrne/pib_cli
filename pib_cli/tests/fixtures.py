"""Test Fixtures for the CLI Commands"""

from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner
from pib_cli.cli.interface import cli_interface as cli


class CommandTestHarness(TestCase):
  __test__ = False
  invocation_command = None
  internal_commands = []
  external_commands = []
  overload = None

  def check_yaml_commands(self, mock_execute):
    if self.external_commands:
      if self.overload is not None:
        mock_execute.assert_called_once_with(
            self.external_commands,
            overload=self.overload,
        )
      else:
        mock_execute.assert_called_once_with(self.external_commands)

  def setUp(self,):
    self.runner = CliRunner()

  @patch('pib_cli.cli.interface.external.execute_external_command')
  @patch('pib_cli.support.container.DevContainer')
  def test_command_invocation_no_overload(
      self,
      mock_container,
      mock_execute,
  ):
    if self.overload is None:
      mock_container.return_value.is_container.return_value = True
      self.runner.invoke(cli, self.invocation_command)

      self.check_yaml_commands(mock_execute)

  @patch('pib_cli.cli.interface.external.execute_external_command')
  @patch('pib_cli.support.container.DevContainer')
  def test_command_invocation_with_overload(
      self,
      mock_container,
      mock_execute,
  ):
    if self.overload is not None:
      mock_container.return_value.is_container.return_value = True
      self.runner.invoke(cli, self.invocation_command + list(self.overload))

      self.check_yaml_commands(mock_execute)
