"""CLI CommandBase test harness."""

import abc
from contextlib import ExitStack
from typing import Optional, Tuple, Type
from unittest import TestCase, mock

from .. import command


class CommandBaseTestHarness(TestCase, abc.ABC):
  """CLI test harness for CommandBase subclasses."""

  __test__ = False
  test_class: Type[command.CommandBase]
  test_exception: Optional[BaseException]
  instance: command.CommandBase
  mock_stack = ExitStack()

  @abc.abstractmethod
  def invoke_command(self) -> Tuple[mock.Mock, ...]:
    """Override to wrap invoke in appropriate patches."""

  def setUp(self) -> None:
    self.instance = self.test_class()
    self.test_exception = None

  @abc.abstractmethod
  def test_invoke(self) -> None:
    """Override to test the invoke class."""
