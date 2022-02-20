"""Test the click CLI container command interfaces."""

from pib_cli.cli.commands import container_setup
from pib_cli.cli.interface.builtins import container
from pib_cli.cli.interface.tests.fixtures import cli_harness


class TestContainerSetupInterface(cli_harness.CliCommandTestHarness):
  """Test the click CLI container setup command interface."""

  cli_command_string = "@pib container setup"
  cli_command_class = container_setup.ContainerSetupCommand
  cli_command_module = container
