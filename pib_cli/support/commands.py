"""CLI Utilities"""

import glob
import os
import shutil
from pathlib import Path

import config
import yaml
from pib_cli import config_filename, project_root
from . import yaml_keys
from .container import ContainerManager
from .paths import PathManager
from .processes import ProcessManager


class Commands:
  overload_env_name = 'PIB_OVERLOAD_ARGUMENTS'
  setup_bash_success = "Setup Succeeded!"

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
    if not ContainerManager.is_container():
      container_only_flag = config.get(yaml_keys.CONTAINER_ONLY, None)
      if container_only_flag is True:
        return True
    return False

  @staticmethod
  def coerce_from_string_to_list(command):
    if isinstance(command, str):
      return [command]
    return command

  @staticmethod
  def setup_bash():
    if not ContainerManager.is_container():
      return config.CONTAINER_ONLY_ERROR
    results = []
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    home_dir = str(Path.home())
    for file_name in bash_files:
      shutil.copy(file_name, home_dir)
      results.append(f"Copied: {file_name} -> {home_dir} ")
    results.append(Commands.setup_bash_success)
    return "\n".join(results)

  def invoke(self, command, overload=None):
    yaml_config = self.__find_config_entry(command)
    if self.__cannot_execute(yaml_config):
      self.process_manager.exit_code = 0
      return config.CONTAINER_ONLY_ERROR

    goto_path = getattr(self.path_manager, yaml_config[yaml_keys.PATH_METHOD])
    goto_path()

    self.__add_overload(overload)

    prepared_command = self.coerce_from_string_to_list(
        yaml_config[yaml_keys.COMMANDS])
    self.process_manager.spawn(prepared_command)

    return yaml_config[self.__translate_response()]
