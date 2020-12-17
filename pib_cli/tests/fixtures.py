"""Test Fixtures"""

from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner
from pib_cli.cli import cli


class CLITestHarness(TestCase):
  __test__ = False
  invocation_command = None
  internal_command = None
  overload = None

  def setUp(self,):
    self.runner = CliRunner()
    self.invocation_command = self.__class__.invocation_command
    self.internal_command = self.__class__.internal_command
    self.overload = self.__class__.overload

  @patch("pib_cli.cli.execute")
  def test_command_invocation_no_overload(self, mock_execute):
    if self.overload is None:
      self.runner.invoke(cli, self.invocation_command)
      mock_execute.assert_called_once_with(self.internal_command)

  @patch("pib_cli.cli.execute")
  def test_command_invocation_with_overload(self, mock_execute):
    if self.overload is not None:
      self.runner.invoke(cli, self.invocation_command + list(self.overload))
      mock_execute.assert_called_once_with(
          self.internal_command,
          overload=self.overload,
      )
