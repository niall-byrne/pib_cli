"""Test harness for CLI commands."""

from typing import Optional
from unittest.mock import patch

from . import cli_harness


class CLIConfigCommandTestHarness(cli_harness.CLICommandTestHarness):
  """Test harness for the CLI interface for configuration commands."""

  handler_expected_argument: Optional[str] = None

  def test_command(self) -> None:
    with patch(self.cli_command_module.__name__ + ".handler") as m_handler:
      self.invoke_cli_command(self.cli_command_string)
      m_handler.assert_called_once_with(
          self.cli_command_class, config_file=self.handler_expected_argument
      )
