"""CLI External Command Management Class"""

import glob
import os
import shutil
from pathlib import Path

from .. import config, project_root
from .configuration import ConfigurationManager
from .container import ContainerManager
from .paths import PathManager
from .processes import ProcessManager


class ExternalCommands:

  def __init__(self):
    self.process_manager = ProcessManager()
    self.path_manager = PathManager()
    self.configuration_manager = ConfigurationManager()

  def __add_overload(self, overload):
    if overload:
      overload_string = " ".join(overload)
      os.environ[config.ENV_OVERLOAD_ARGUMENTS] = overload_string

  def __change_directory(self):
    yaml_path_method = self.configuration_manager.get_config_path_method()
    goto_path = getattr(self.path_manager, yaml_path_method)
    goto_path()

  def __spawn_commands(self):
    yaml_commands = self.configuration_manager.get_config_commands()
    self.process_manager.spawn(yaml_commands)
    return self.process_manager.exit_code

  @staticmethod
  def setup_bash():
    if not ContainerManager.is_container():
      return config.ERROR_CONTAINER_ONLY
    results = []
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    home_dir = str(Path.home())
    for file_name in bash_files:
      shutil.copy(file_name, home_dir)
      results.append(f"Copied: {file_name} -> {home_dir} ")
    results.append(config.SETTING_BASH_SETUP_SUCCESS_MESSAGE)
    return "\n".join(results)

  def invoke(self, command, overload=None):
    self.configuration_manager.find_config_entry(command)

    if not self.configuration_manager.is_config_executable():
      self.process_manager.exit_code = 0
      return config.ERROR_CONTAINER_ONLY

    self.__change_directory()
    self.__add_overload(overload)
    exit_code = self.__spawn_commands()

    return self.configuration_manager.get_config_response(exit_code)
