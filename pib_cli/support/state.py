"""State class."""

from typing import Any, Dict, cast

from pib_cli.support.user_configuration import user_configuration_file
from pib_cli.support.user_configuration.bases import user_configuration_base


class State:
  """Monostate of the current running configuration."""

  __shared_state: Dict[str, Any] = {}

  def __init__(self) -> None:
    self.__dict__ = self.__shared_state
    if not self.__shared_state:
      self.user_config_file = cast(
          user_configuration_file.UserConfigurationFile,
          None,
      )
      self.user_config = cast(
          user_configuration_base.UserConfigurationVersionBase,
          None,
      )

  @classmethod
  def clear(cls) -> None:
    """Reset the internal state back to default for future instances."""

    cls.__shared_state = {}

  def load(self) -> None:
    """Populate the monostate with configuration values."""

    self.user_config_file = user_configuration_file.UserConfigurationFile()
    self.user_config = self.user_config_file.parse()
