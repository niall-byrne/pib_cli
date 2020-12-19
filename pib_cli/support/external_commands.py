"""CLI External Command Management Class"""

import sys

import click

from .. import config
from .configuration import ConfigurationManager
from .paths import PathManager
from .processes import ProcessManager


class ExternalCommands:

  def __init__(self):
    self.process_manager = ProcessManager()
    self.path_manager = PathManager()
    self.configuration_manager = ConfigurationManager()

  def __change_directory(self):
    yaml_path_method = self.configuration_manager.get_config_path_method()
    goto_path = getattr(self.path_manager, yaml_path_method)
    goto_path()

  def __spawn_commands(self, overload):
    yaml_commands = self.configuration_manager.get_config_commands()
    self.process_manager.spawn(yaml_commands, overload)
    return self.process_manager.exit_code

  def invoke(self, command, overload):
    self.configuration_manager.find_config_entry(command)

    if not self.configuration_manager.is_config_executable():
      self.process_manager.exit_code = 0
      return config.ERROR_CONTAINER_ONLY

    self.__change_directory()
    exit_code = self.__spawn_commands(overload)

    return self.configuration_manager.get_config_response(exit_code)


def execute_external_command(commands, overload=None):
  """Executes a batch of external commands.

  commands: A list of commands to be executed
  overload: Additional parameters which will be inserted into the environment
  """

  command_manager = ExternalCommands()

  for command in commands:
    response = command_manager.invoke(command, overload)
    click.echo(response)

    if command_manager.process_manager.exit_code != 0:
      break

  sys.exit(command_manager.process_manager.exit_code)
