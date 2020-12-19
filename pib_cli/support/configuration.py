"""Configuration Management Class"""

import yaml
from config import yaml_keys

from .. import config_filename
from .container import ContainerManager


class ConfigurationManager:

  def __init__(self):
    with open(config_filename) as file_handle:
      self.config = yaml.safe_load(file_handle)
    self.config_entry = None

  def __coerce_command_string_to_list(self):
    commands = self.config_entry[yaml_keys.COMMANDS]
    if isinstance(commands, str):
      self.config_entry[yaml_keys.COMMANDS] = [commands]

  def find_config_entry(self, command_name):
    for entry in self.config:
      if entry[yaml_keys.COMMAND_NAME] == command_name:
        self.config_entry = entry
        self.__coerce_command_string_to_list()
        return
    raise KeyError("Could not find yaml key name: %s" % command_name)

  def get_config_path_method(self):
    return self.config_entry[yaml_keys.PATH_METHOD]

  def get_config_commands(self):
    return self.config_entry[yaml_keys.COMMANDS]

  def get_config_response(self, exit_code):
    if exit_code == 0:
      return self.config_entry[yaml_keys.SUCCESS]
    return self.config_entry[yaml_keys.FAILURE]

  def is_config_executable(self):
    if not ContainerManager.is_container():
      container_only_flag = self.config_entry.get(
          yaml_keys.CONTAINER_ONLY,
          None,
      )
      if container_only_flag is True:
        return False
    return True
