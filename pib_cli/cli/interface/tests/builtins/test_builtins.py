"""Test the click CLI builtin command interfaces."""

from pib_cli.cli.commands import version
from pib_cli.cli.interface import builtins
from pib_cli.cli.interface.tests.fixtures import cli_harness


class TestVersionInterface(cli_harness.CLICommandTestHarness):
  """Test the click CLI version command interface."""

  cli_command_string = "@pib version"
  cli_command_class = version.VersionCommand
  cli_command_module = builtins
