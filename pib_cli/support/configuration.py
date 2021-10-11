"""Configuration Management Class."""

import json
from pathlib import Path

import yaml
from jsonschema import validate

from .. import config, config_filename
from ..config import yaml_keys
from .dev_container import DevContainer


class ConfigurationManager:
  """Manages access to the yaml configuration."""

  schema_file = Path(config.__file__).parent / "schema.json"

  def __init__(self):
    self.schema = self._load_schema()
    self.config = self._load_config()

    self._validate()
    self.config_entry = None

  def _load_schema(self):
    with open(self.schema_file, encoding='utf-8') as file_handle:
      schema = json.load(file_handle)
    return schema

  def _load_config(self):
    with open(config_filename, encoding='utf-8') as file_handle:
      configuration_file_content = yaml.safe_load(file_handle)
    return configuration_file_content

  def _validate(self):
    validate(self.config, self.schema)

  def _coerce_command_string_to_list(self):
    commands = self.config_entry[yaml_keys.COMMANDS]
    if isinstance(commands, str):
      self.config_entry[yaml_keys.COMMANDS] = [commands]

  def find_config_entry(self, command_name):
    """Select the configuration entry of the specified command.

    :param command_name: The name of the yaml command to select
    :type command_name: basestring
    :raises: KeyError
    """
    for entry in self.config:
      if entry[yaml_keys.COMMAND_NAME] == command_name:
        self.config_entry = entry
        self._coerce_command_string_to_list()
        return
    raise KeyError("Could not find yaml key name: %s" % command_name)

  def get_config_path_method(self):
    """Return the path method associated with the selected yaml config.
    (:class:`pib_cli.support.paths.PathManager`)

    :returns: The name of the path method from the selected yaml config
    :rtype: basestring
    """
    return self.config_entry[yaml_keys.PATH_METHOD]

  def get_config_commands(self):
    """Return the commands section of the selected yaml config.

    :returns: A list of commands from the selected yaml config
    :rtype: list[basestring]
    """
    return self.config_entry[yaml_keys.COMMANDS]

  def get_config_response(self, exit_code):
    """Return the response message content based on the command exit code.

    :param exit_code: The exit code returned by a process
    :type exit_code: int
    :returns: The response message for the given exit_code
    :rtype: list[basestring]
    """
    if exit_code == 0:
      return self.config_entry[yaml_keys.SUCCESS]
    return self.config_entry[yaml_keys.FAILURE]

  def is_config_executable(self):
    """Determine if the currently selected command can be executed or not.

    :returns: A boolean indicating if the command can currently be executed
    :rtype: bool
    """
    if not DevContainer.is_container():
      container_only_flag = self.config_entry.get(
          yaml_keys.CONTAINER_ONLY,
          None,
      )
      if container_only_flag is True:
        return False
    return True
