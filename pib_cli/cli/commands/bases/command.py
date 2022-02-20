"""PIB CLI base command class."""

import abc


class CommandBase(abc.ABC):
  """An generic, invokable command."""

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke this command."""
