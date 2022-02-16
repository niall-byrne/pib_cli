"""UserConfiguration class."""

from pib_cli.support.mixins import yaml_file

from ... import config_filename
from ...config import yaml_keys
from . import selected, validator


class UserConfiguration(yaml_file.YAMLFileReader):
  """The entire user defined pib_cli configuration."""

  def __init__(self) -> None:
    self.validator = validator.UserConfigurationValidator()
    self.config = self.load_yaml_file(config_filename)
    self.validator.validate(self.config)

  def select_config_entry(
      self, command_name: str
  ) -> selected.SelectedUserConfigurationEntry:
    """Select the configuration entry of the specified command.

    :param command_name: The name of the yaml command to select
    :returns: A Python representation of the selected configuration.
    :raises: KeyError
    """
    for entry in self.config:
      if entry[yaml_keys.COMMAND_NAME] == command_name:
        return selected.SelectedUserConfigurationEntry(entry)
    raise KeyError("Could not find command named: %s" % command_name)
