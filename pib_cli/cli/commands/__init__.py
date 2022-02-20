"""PIB CLI command class definitions."""

from typing import Type

from .bases.command import CommandBase


def handler(command_class: Type[CommandBase]) -> None:
  """Invoke a CommandBase subclass."""

  command = command_class()
  command.invoke()
