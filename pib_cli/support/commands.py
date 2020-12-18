"""CLI Utilities"""

import os

import yaml
from pib_cli import config_filename
from . import yaml_keys
from .paths import PathManager
from .processes import ProcessManager


class Commands:
  overload_env_name = 'PIB_OVERLOAD_ARGUMENTS'
  container_only_error = "This command can only be run inside a PIB container."

  def __init__(self):
    self.process_manager = ProcessManager()
    self.path_manager = PathManager()
    with open(config_filename) as file_handle:
      self.config = yaml.safe_load(file_handle)

  def __find_config_entry(self, name):
    for entry in self.config:
      if entry[yaml_keys.COMMAND_NAME] == name:
        return entry
    raise KeyError("Could not find yaml key name: %s" % name)

  def __add_overload(self, overload):
    if overload:
      overload_string = " ".join(overload)
      os.environ[self.__class__.overload_env_name] = overload_string

  def __translate_response(self):
    if self.process_manager.exit_code == 0:
      return yaml_keys.SUCCESS
    return yaml_keys.FAILURE

  def __cannot_execute(self, config):
    if not self.path_manager.is_container():
      container_only_flag = config.get(yaml_keys.CONTAINER_ONLY, None)
      if container_only_flag is True:
        return True
    return False

  @staticmethod
  def coerce_from_string_to_list(command):
    if isinstance(command, str):
      return [command]
    return command

  def invoke(self, command, overload=None):
    config = self.__find_config_entry(command)
    if self.__cannot_execute(config):
      return self.__class__.container_only_error

    goto_path = getattr(self.path_manager, config[yaml_keys.PATH_METHOD])
    goto_path()

    self.__add_overload(overload)

    prepared_command = self.coerce_from_string_to_list(
        config[yaml_keys.COMMANDS])
    self.process_manager.spawn(prepared_command)

    return config[self.__translate_response()]
