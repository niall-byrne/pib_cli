"""CLI External Command Management Class."""

import sys

import click

from .. import config
from .configuration import ConfigurationManager
from .paths import get_path_manager
from .processes import ProcessManager


class ExternalCommands:
  """Methods for managing external yaml configured commands."""

  def __init__(self):
    self.process_manager = ProcessManager()
    self.path_manager = get_path_manager()
    self.configuration_manager = ConfigurationManager()

  def __change_directory(self):
    """Extract the correct method from the yaml configuration and call it."""

    yaml_path_method = self.configuration_manager.get_config_path_method()
    goto_path = getattr(self.path_manager, yaml_path_method)
    goto_path()

  def __spawn_commands(self, overload):
    """Extract the correct series of commands from the yaml configuration.

    (calls :func:`pib_cli.support.processes.ProcessManager.spawn`)

    :param overload: Extra overloaded arguments specified at the CLI
    :type overload: tuple[basestring]
    :returns: The resulting exit code of the process
    :rtype: int
    """
    yaml_commands = self.configuration_manager.get_config_commands()
    self.process_manager.spawn(yaml_commands, overload)
    return self.process_manager.exit_code

  def invoke(self, command, overload):
    """Read the yaml configuration of the given command, and executes it.

    :param command: The name of the yaml configured command to execute
    :type command: basestring
    :param overload: Extra overloaded arguments specified at the CLI
    :type overload: tuple[basestring]
    :returns: The response message from the yaml configuration
    :rtype: basestring
    """
    self.configuration_manager.find_config_entry(command)

    if not self.configuration_manager.is_config_executable():
      self.process_manager.exit_code = 0
      return config.ERROR_CONTAINER_ONLY

    self.__change_directory()
    exit_code = self.__spawn_commands(overload)

    return self.configuration_manager.get_config_response(exit_code)


def execute_external_command(commands, overload=None):
  """Execute a batch of yaml configured commands.

  :param commands: A list of commands to be executed
  :type commands: list[basestring]
  :param overload: Extra overloaded arguments specified at the CLI
  :type overload: tuple[basestring]
  """
  command_manager = ExternalCommands()

  for command in commands:
    response = command_manager.invoke(command, overload)
    click.echo(response)

    if command_manager.process_manager.exit_code != 0:
      break

  sys.exit(command_manager.process_manager.exit_code)
