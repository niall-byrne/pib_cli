"""CLI CommandBase test harness."""

import abc
from typing import Type
from unittest import TestCase, mock

from .. import command


class CommandBaseTestHarness(TestCase, abc.ABC):
  """CLI test harness for CommandBase subclasses."""

  __test__ = False
  test_class: Type[command.CommandBase]

  def setUp(self) -> None:
    self.instance = self.test_class()

  @abc.abstractmethod
  def test_invoke(self, m_module: mock.Mock) -> None:
    """Override to test the invoke class."""
