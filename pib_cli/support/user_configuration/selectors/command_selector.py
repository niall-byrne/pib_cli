"""CommandSelector class."""

from pib_cli.config import yaml_keys

from ..bases.command_selector_base import CommandSelectorBase


class CommandSelector(CommandSelectorBase):
  """A parsed end-user configuration entry, ready to use.

  :param user_configuration: A Python object for the YAML configuration.
  """

  user_configuration: yaml_keys.TypeUserConfiguration

  def __init__(
      self, user_configuration: yaml_keys.TypeUserConfiguration
  ) -> None:
    super().__init__(user_configuration)

  def get_config_path_method(self) -> str:
    """Return the path method associated with the selected yaml config.

    :returns: The name of the path method from the selected yaml config.
    """
    return self.user_configuration[yaml_keys.PATH_METHOD]
