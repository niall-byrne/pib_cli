"""CLI CommandBase test harness with exception handling."""

import abc
from typing import Optional, Type, Union

from .command_harness import CommandBaseTestHarness


class CommandBaseExceptionsTestHarness(CommandBaseTestHarness, abc.ABC):
  """CLI test harness for CommandBase subclasses with exceptions."""

  __test__ = False

  def setUp(self) -> None:
    super().setUp()
    self.side_effect: Optional[Union[Type[BaseException], BaseException]] = None

  @abc.abstractmethod
  def test_invoke_exception(self) -> None:
    """Override to test the invoke class with an exception case."""
