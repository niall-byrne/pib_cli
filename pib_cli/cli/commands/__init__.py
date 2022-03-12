"""PIB CLI command class definitions."""

from typing import Optional, Type, Union

from .bases.command import CommandBase
from .bases.command_config import CommandConfigBase


def handler(
    command_class: Type[Union[CommandBase, CommandConfigBase]],
    config_file: Optional[str] = None,
) -> None:
  """Invoke a CommandBase subclass."""

  command: Union[CommandBase, CommandConfigBase]

  if issubclass(command_class, CommandConfigBase):
    command = command_class(config_file=config_file)
  else:
    command = command_class()

  command.invoke()
