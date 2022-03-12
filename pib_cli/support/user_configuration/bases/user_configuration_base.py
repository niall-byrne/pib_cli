"""UserConfigurationBase class."""

import abc
from typing import Any, Dict, List

from pib_cli.config import yaml_keys

from .. import selected


class UserConfigurationVersionBase:
  """The base class for a schema version of pib_cli configurations."""

  version: str

  def __init__(self, configuration: Any) -> None:
    self.configuration = configuration
    self.configuration_command_index = self._create_command_index()
    self.project_name = self.get_project_name()

  def _create_command_index(self) -> Dict[str, yaml_keys.TypeUserConfiguration]:
    index: Dict[str, yaml_keys.TypeUserConfiguration] = {}
    for entry in self.get_command_definitions():
      index[entry[yaml_keys.COMMAND_NAME]] = entry
    return index

  @abc.abstractmethod
  def get_project_name(self) -> str:
    """Return the project name from the configuration."""

  @abc.abstractmethod
  def get_command_definitions(self) -> List[Any]:
    """Return the CLI command definitions from the configuration."""

  def select_config_entry(
      self, command_name: str
  ) -> selected.SelectedUserConfigurationEntry:
    """Select the configuration entry of the specified command.

    :param command_name: The name of the command to select
    :returns: A Python representation of the selected configuration.
    :raises: KeyError
    """
    try:
      entry = self.configuration_command_index[command_name]
      return selected.SelectedUserConfigurationEntry(entry)
    except KeyError as exc:
      raise KeyError("Could not find command named: %s" % command_name) from exc
