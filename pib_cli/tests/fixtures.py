"""Test Fixtures"""

from unittest import TestCase
from unittest.mock import patch

import patchbay
from click.testing import CliRunner
from pib_cli.cli import cli


class CommandTestHarness(TestCase):
  __test__ = False
  invocation_command = None
  python_methods = []
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

  def check_internal_commands(self, mock_setup_bash):
    if 'setup_bash' in self.python_methods:
      mock_setup_bash.assert_called_once_with()

  def setUp(self,):
    self.runner = CliRunner()
    self.invocation_command = self.__class__.invocation_command
    self.python_methods = self.__class__.python_methods
    self.external_commands = self.__class__.external_commands
    self.overload = self.__class__.overload

  @patch(patchbay.CLI_PIB_CLI_EXECUTE)
  @patch(patchbay.COMMANDS_IS_CONTAINER)
  @patch(patchbay.COMMANDS_SETUP_BASH)
  def test_command_invocation_no_overload(
      self,
      mock_setup_bash,
      mock_container,
      mock_execute,
  ):
    if self.overload is None:
      mock_container.return_value = True
      self.runner.invoke(cli, self.invocation_command)

      self.check_yaml_commands(mock_execute)
      self.check_internal_commands(mock_setup_bash)

  @patch(patchbay.CLI_PIB_CLI_EXECUTE)
  @patch(patchbay.COMMANDS_IS_CONTAINER)
  @patch(patchbay.COMMANDS_SETUP_BASH)
  def test_command_invocation_with_overload(
      self,
      mock_setup_bash,
      mock_container,
      mock_execute,
  ):
    if self.overload is not None:
      mock_container.return_value = True
      self.runner.invoke(cli, self.invocation_command + list(self.overload))

      self.check_yaml_commands(mock_execute)
      self.check_internal_commands(mock_setup_bash)
