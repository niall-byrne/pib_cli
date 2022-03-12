"""Configuration managed CLI commands."""

import copy

import click
from pib_cli.config.locale import _
from pib_cli.support import state
from pib_cli.support.iterators import cli_custom_commands


@click.group(_("configuration_commands"))
def document_custom_commands() -> None:
  """Click group of all custom defined commands."""


def load_custom_commands() -> click.Group:
  """Create and attach the custom commands to the click group.

  :returns: The click group, with all custom commands attached.
  """

  state.State().load()
  for custom_command in cli_custom_commands.CustomClickCommandIterator():
    document_custom_commands.add_command(custom_command)
  return document_custom_commands


# Create a copy of the click group to allow Sphinx to reference the original
custom_commands: click.Group = copy.deepcopy(load_custom_commands())
