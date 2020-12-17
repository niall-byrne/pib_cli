"""CLI Utilities"""

import yaml
from pib_cli import config_filename
from .paths import PathManager
from .processes import ProcessManager


class Commands:

  def __init__(self):
    self.process_manager = ProcessManager()
    self.path_manager = PathManager()
    with open(config_filename) as file_handle:
      self.config = yaml.load(file_handle, Loader=yaml.FullLoader)

  def __find_config_entry(self, name):
    for entry in self.config:
      if entry['name'] == name:
        return entry
    raise KeyError("Could not find yaml key name: %s" % name)

  def invoke(self, command):
    config = self.__find_config_entry(command)
    goto_path = getattr(self.path_manager, config['path_method'])

    goto_path()
    self.process_manager.spawn(config['commands'])

    if self.process_manager.exit_code == 0:
      return config['success']
    return config['failure']
