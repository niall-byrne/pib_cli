"""Test Fixtures"""

from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner

from .. import patchbay
from ..cli import cli


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

  def check_internal_commands(self, mock_internal):
    if self.internal_commands:
      mock_internal.assert_called_once_with(self.internal_commands)

  def setUp(self,):
    self.runner = CliRunner()
    self.invocation_command = self.__class__.invocation_command
    self.internal_commands = self.__class__.internal_commands
    self.external_commands = self.__class__.external_commands
    self.overload = self.__class__.overload

  @patch(patchbay.CLI_EXECUTE_EXTERNAL_COMMAND)
  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER)
  @patch(patchbay.CLI_EXECUTE_INTERNAL_COMMAND)
  def test_command_invocation_no_overload(
      self,
      mock_internal,
      mock_container,
      mock_execute,
  ):
    if self.overload is None:
      mock_container.return_value = True
      mock_internal.return_value = "Success Message"
      self.runner.invoke(cli, self.invocation_command)

      self.check_yaml_commands(mock_execute)
      self.check_internal_commands(mock_internal)

  @patch(patchbay.CLI_EXECUTE_EXTERNAL_COMMAND)
  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER)
  @patch(patchbay.CLI_EXECUTE_INTERNAL_COMMAND)
  def test_command_invocation_with_overload(
      self,
      mock_internal,
      mock_container,
      mock_execute,
  ):
    if self.overload is not None:
      mock_container.return_value = True
      mock_internal.return_value = "Success Message"
      self.runner.invoke(cli, self.invocation_command + list(self.overload))

      self.check_yaml_commands(mock_execute)
      self.check_internal_commands(mock_internal)
