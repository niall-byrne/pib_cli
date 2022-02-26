"""Test the click CLI container command interfaces."""

from pib_cli.cli.commands import (
    container_setup,
    container_validate,
    container_version,
)
from pib_cli.cli.interface.builtins import container
from pib_cli.cli.interface.tests.fixtures import cli_harness


class TestContainerSetupInterface(cli_harness.CLICommandTestHarness):
  """Test the click CLI container setup command interface."""

  cli_command_string = "@pib container setup"
  cli_command_class = container_setup.ContainerSetupCommand
  cli_command_module = container


class TestContainerValidateInterface(cli_harness.CLICommandTestHarness):
  """Test the click CLI container validate command interface."""

  cli_command_string = "@pib container validate"
  cli_command_class = container_validate.ContainerValidateCommand
  cli_command_module = container


class TestContainerVersionInterface(cli_harness.CLICommandTestHarness):
  """Test the click CLI container version command interface."""

  cli_command_string = "@pib container version"
  cli_command_class = container_version.ContainerVersionCommand
  cli_command_module = container
