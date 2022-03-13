"""Borg monostate of the current running configuration."""

from typing import Any, Dict, cast

from pib_cli.support import user_configuration


class State:
  """Monostate of the current running configuration."""

  __shared_state: Dict[str, Any] = {}

  def __init__(self) -> None:
    self.__dict__ = self.__shared_state
    if not self.__shared_state:
      self.user_config = cast(user_configuration.UserConfiguration, None)

  @classmethod
  def clear(cls) -> None:
    """Reset the internal state back to default for future instances."""

    cls.__shared_state = {}

  def load(self) -> None:
    """Populate the monostate with configuration values."""

    configuration = user_configuration.UserConfiguration()
    configuration.validate()
    self.user_config = configuration
