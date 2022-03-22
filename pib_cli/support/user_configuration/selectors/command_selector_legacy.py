"""LegacyCommandSelector class."""

from typing import Dict

from pib_cli.config import yaml_keys

from ..bases.command_selector_base import CommandSelectorBase


class LegacyCommandSelector(CommandSelectorBase):
  """A parsed end-user legacy configuration entry, ready to use.

  :param user_configuration: A Python object for the YAML configuration.
  """

  user_configuration: yaml_keys.TypeLegacyUserConfiguration
  legacy_path_method_mapping: Dict[str, str] = {
      "project_docs": "documentation_root",
      "project_root": "git_root",
      "project_home": "project_root",
  }

  def __init__(
      self, user_configuration: yaml_keys.TypeLegacyUserConfiguration
  ) -> None:
    super().__init__(user_configuration)
    self.user_configuration[yaml_keys.DESCRIPTION] = ""

  def get_config_path_method(self) -> str:
    """Return the path method associated with the selected yaml config.

    :returns: The name of the path method from the selected yaml config.
    """
    return self.legacy_path_method_mapping[self.user_configuration[
        yaml_keys.LEGACY_PATH_METHOD]]
