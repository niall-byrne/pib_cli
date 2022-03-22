"""Test harness for the custom CLI commands."""

from typing import cast
from unittest.mock import Mock, patch

from pib_cli.cli.interface.custom import cli_custom_commands
from pib_cli.support.user_configuration import user_configuration_file
from pib_cli.support.user_configuration.selectors import command_selector

from . import cli_harness


class CustomCLIInterfaceTestHarness(cli_harness.CLICommandTestHarness):
  """Test harness for the custom CLI interface."""

  __test__ = False
  cli_command_string: str

  def select_default_config(self) -> command_selector.CommandSelector:
    default_config = self.default_config.configuration_command_index[
        self.cli_command_string]
    selected_default_config = command_selector.CommandSelector(default_config)
    return selected_default_config

  def setUp(self) -> None:
    self.default_config = \
      user_configuration_file.UserConfigurationFile().parse()

  def invoke_custom_command(self) -> Mock:
    with patch(
        cli_custom_commands.__name__ + ".customized.CustomizedCommand"
    ) as m_command:
      self.invoke_cli_command(self.cli_command_string)
    return m_command

  def test_command(self) -> None:
    m_command = self.invoke_custom_command()
    _, kwargs = m_command.call_args
    config_object = cast(
        command_selector.CommandSelector, kwargs['command_configuration']
    )

    self.assertDictEqual(
        self.select_default_config().user_configuration,
        config_object.user_configuration
    )
