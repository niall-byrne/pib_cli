"""State class."""

from typing import Any, Dict, cast

import click
from pib_cli.config.locale import _
from pib_cli.support.user_configuration import user_configuration_file
from pib_cli.support.user_configuration.bases import version_base


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
          version_base.UserConfigurationVersionBase,
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
    self._default_config_warning()

  def _default_config_warning(self) -> None:
    config_file_in_use = self.user_config_file.get_config_file_name()
    if self.user_config_file.default_config == config_file_in_use:
      click.echo(_("** PIB DEFAULT CONFIG IN USE **"))
