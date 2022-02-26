"""Test harness for CLI commands."""

from types import ModuleType
from typing import Type
from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner
from pib_cli.cli.commands.bases.command import CommandBase
from pib_cli.cli.interface import cli_interface


class CLICommandTestHarness(TestCase):
  """Test harness for the CLI interface."""

  cli_command_module: ModuleType
  cli_command_string: str
  cli_command_class: Type[CommandBase]

  def invoke_cli_command(self, cmd: str) -> None:
    runner = CliRunner()
    runner.invoke(cli_interface, cmd)

  def test_command(self) -> None:
    with patch(self.cli_command_module.__name__ + ".handler") as m_handler:
      self.invoke_cli_command(self.cli_command_string)
      m_handler.assert_called_once_with(self.cli_command_class)
