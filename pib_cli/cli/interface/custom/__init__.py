"""Configuration managed CLI commands."""

import copy

import click
from pib_cli.support.iterators import cli_custom_commands


@click.group("configuration_commands")
def defined_with_user_configuration() -> None:
  """Stub for testing custom commands during development."""


for custom_command in cli_custom_commands.CustomClickCommandIterator():
  defined_with_user_configuration.add_command(custom_command)

# Create a copy of the click group to allow Sphinx to reference the original
custom_commands: click.Group = copy.deepcopy(defined_with_user_configuration)
