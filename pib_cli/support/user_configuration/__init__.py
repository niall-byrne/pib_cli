"""UserConfiguration class."""

from typing import Dict

from pib_cli import config_filename
from pib_cli.config import yaml_keys
from pib_cli.support.mixins import text_file, yaml_file

from . import selected, validator


class UserConfiguration(yaml_file.YAMLFileReader, text_file.TextFileReader):
  """The entire user defined pib_cli configuration."""

  def __init__(self) -> None:
    self.configuration_validator = validator.UserConfigurationValidator()
    self.configuration = self.load_yaml_file(config_filename)
    self.configuration_command_index = self._create_command_index()

  def _create_command_index(self) -> Dict[str, yaml_keys.TypeUserConfiguration]:
    index: Dict[str, yaml_keys.TypeUserConfiguration] = {}
    for entry in self.configuration:
      index[entry[yaml_keys.COMMAND_NAME]] = entry
    return index

  def get_raw_file(self) -> str:
    """Return the original configuration file from disk."""
    return self.load_text_file(config_filename).rstrip()

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

  def validate(self) -> None:
    """Validate the user configuration."""

    self.configuration_validator.validate(self.configuration)
