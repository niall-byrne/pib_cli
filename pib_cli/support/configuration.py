"""Configuration Management Class"""

import yaml

from .. import config_filename
from ..config import yaml_keys
from .container import ContainerManager


class ConfigurationManager:
  """Manages access to the yaml configuration."""

  def __init__(self):
    with open(config_filename) as file_handle:
      self.config = yaml.safe_load(file_handle)
    self.config_entry = None

  def __coerce_command_string_to_list(self):
    """Converts the yaml data for the key of commands into a list if it is
    entered as a string."""
    commands = self.config_entry[yaml_keys.COMMANDS]
    if isinstance(commands, str):
      self.config_entry[yaml_keys.COMMANDS] = [commands]

  def find_config_entry(self, command_name):
    """Selects the configuration entry of the specified command.

    :param command_name: The name of the yaml command to select
    :type command_name: basestring
    :raises: KeyError
    """
    for entry in self.config:
      if entry[yaml_keys.COMMAND_NAME] == command_name:
        self.config_entry = entry
        self.__coerce_command_string_to_list()
        return
    raise KeyError("Could not find yaml key name: %s" % command_name)

  def get_config_path_method(self):
    """Returns the path method associated with the selected yaml config.
    (:class:`pib_cli.support.paths.PathManager`)

    :returns: The name of the path method from the selected yaml config
    :rtype: basestring
    """
    return self.config_entry[yaml_keys.PATH_METHOD]

  def get_config_commands(self):
    """Returns the commands section of the selected yaml config.

    :returns: A list of commands from the selected yaml config
    :rtype: list[basestring]
    """
    return self.config_entry[yaml_keys.COMMANDS]

  def get_config_response(self, exit_code):
    """Returns the yaml configuraton for a sucessful or unsuccessful execution
    of the associated command.

    :param exit_code: The exit code returned by a process
    :type exit_code: int
    :returns: The response message for the given exit_code
    :rtype: list[basestring]
    """
    if exit_code == 0:
      return self.config_entry[yaml_keys.SUCCESS]
    return self.config_entry[yaml_keys.FAILURE]

  def is_config_executable(self):
    """Determines if the currently selected command can be executed or not.

    :returns: A boolean indicating if the command can currently be executed
    :rtype: bool
    """
    if not ContainerManager.is_container():
      container_only_flag = self.config_entry.get(
          yaml_keys.CONTAINER_ONLY,
          None,
      )
      if container_only_flag is True:
        return False
    return True
