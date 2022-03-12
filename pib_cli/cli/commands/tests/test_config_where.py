"""Test the ConfigWhereCommand class."""

from typing import Optional, Tuple, Type
from unittest.mock import Mock, patch

from .. import config_where
from ..bases.fixtures import command_harness_config


class TestConfigWhereCommand(
    command_harness_config.CommandConfigBaseTestHarness
):
  """Test the ConfigWhereCommand class."""

  __test__ = True
  test_class: Type[config_where.ConfigWhereCommand]
  instance: config_where.ConfigWhereCommand

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = config_where.ConfigWhereCommand

  def invoke_command(self, config_file: Optional[str]) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_config = self.create_instance(config_file=config_file)
      m_click = stack.enter_context(patch(config_where.__name__ + ".click"))
      self.instance.invoke()
    return m_click, m_config

  def test_invoke_default(self) -> None:
    m_click, m_config = self.invoke_command(config_file=None)
    m_config.assert_called_once_with(config_file=None)
    path = m_config.return_value.get_config_file_name.return_value
    m_click.echo.assert_called_once_with(f"Configuration file: {path}")

  def test_invoke_with_config(self) -> None:
    m_click, m_config = self.invoke_command(config_file=self.mock_config_file)
    m_config.assert_called_once_with(config_file=self.mock_config_file)
    path = m_config.return_value.get_config_file_name.return_value
    m_click.echo.assert_called_once_with(f"Configuration file: {path}")
