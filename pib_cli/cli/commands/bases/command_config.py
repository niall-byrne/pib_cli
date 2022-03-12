"""PIB CLI base config command class."""

import abc
from typing import Optional

from pib_cli.support.user_configuration import user_configuration_file

from .command import CommandBase


class CommandConfigBase(CommandBase, abc.ABC):
  """An invokable command with a specified configuration file.

  :param config_file: The specified file to use, instead of the default.
  """

  def __init__(self, config_file: Optional[str] = None) -> None:
    self.user_config_file = user_configuration_file.UserConfigurationFile(
        config_file=config_file
    )
