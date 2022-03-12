"""CLI CommandConfigBase test harness."""

import abc
from contextlib import ExitStack
from typing import Optional, Tuple, Type
from unittest import TestCase, mock

from .. import command_config


class CommandConfigBaseTestHarness(TestCase, abc.ABC):
  """CLI test harness for CommandConfigBase subclasses."""

  __test__ = False
  test_class: Type[command_config.CommandConfigBase]
  instance: command_config.CommandConfigBase
  mock_stack = ExitStack()

  def setUp(self) -> None:
    self.mock_config_file = "./app/config"

  def create_instance(self, config_file: Optional[str]) -> mock.Mock:
    with mock.patch(
        command_config.__name__ +
        ".user_configuration_file.UserConfigurationFile"
    ) as m_config:
      self.instance = self.test_class(config_file=config_file)
    return m_config

  @abc.abstractmethod
  def invoke_command(self, config_file: Optional[str]) -> Tuple[mock.Mock, ...]:
    """Override to wrap invoke in appropriate patches."""

  @abc.abstractmethod
  def test_invoke_default(self) -> None:
    """Override to test the invoke class."""

  @abc.abstractmethod
  def test_invoke_with_config(self) -> None:
    """Override to test the invoke class."""
