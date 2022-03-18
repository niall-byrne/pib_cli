"""Test the click CLI config command interfaces."""

from pib_cli.cli.commands import (
    config_show,
    config_validate,
    config_version,
    config_where,
)
from pib_cli.cli.interface.builtins import config
from pib_cli.cli.interface.tests.fixtures import config_cli_harness


class TestConfigShowInterface(config_cli_harness.CLIConfigCommandTestHarness):
  """Test the click CLI config show command interface."""

  cli_command_string = "@pib config show"
  cli_command_class = config_show.ConfigShowCommand
  cli_command_module = config


class TestConfigShowInterfaceArgs(
    config_cli_harness.CLIConfigCommandTestHarness
):
  """Test the click CLI config show command interface with arguments."""

  cli_command_string = "@pib config -c assets/cli.yml show"
  cli_command_class = config_show.ConfigShowCommand
  cli_command_module = config
  handler_expected_argument = "assets/cli.yml"


class TestConfigValidateInterface(
    config_cli_harness.CLIConfigCommandTestHarness
):
  """Test the click CLI config validate command interface."""

  cli_command_string = "@pib config validate"
  cli_command_class = config_validate.ConfigValidateCommand
  cli_command_module = config


class TestConfigValidateInterfaceArgs(
    config_cli_harness.CLIConfigCommandTestHarness
):
  """Test the click CLI config validate command interface with arguments."""

  cli_command_string = "@pib config -c assets/cli.yml validate"
  cli_command_class = config_validate.ConfigValidateCommand
  cli_command_module = config
  handler_expected_argument = "assets/cli.yml"


class TestConfigVersionInterface(
    config_cli_harness.CLIConfigCommandTestHarness
):
  """Test the click CLI config version command interface."""

  cli_command_string = "@pib config version"
  cli_command_class = config_version.ConfigVersionCommand
  cli_command_module = config


class TestConfigVersionInterfaceArgs(
    config_cli_harness.CLIConfigCommandTestHarness
):
  """Test the click CLI config version command interface with arguments."""

  cli_command_string = "@pib config -c assets/cli.yml version"
  cli_command_class = config_version.ConfigVersionCommand
  cli_command_module = config
  handler_expected_argument = "assets/cli.yml"


class TestConfigWhereInterface(config_cli_harness.CLIConfigCommandTestHarness):
  """Test the click CLI config where command interface."""

  cli_command_string = "@pib config where"
  cli_command_class = config_where.ConfigWhereCommand
  cli_command_module = config


class TestConfigWhereInterfaceArgs(
    config_cli_harness.CLIConfigCommandTestHarness
):
  """Test the click CLI config where command interface with arguments."""

  cli_command_string = "@pib config -c assets/cli.yml where"
  cli_command_class = config_where.ConfigWhereCommand
  cli_command_module = config
  handler_expected_argument = "assets/cli.yml"
