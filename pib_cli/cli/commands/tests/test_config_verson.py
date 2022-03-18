"""Test the ConfigVersionCommand class."""

from typing import Optional, Tuple, Type
from unittest.mock import Mock, patch

from .. import config_version
from ..bases.fixtures import command_harness_config


class TestConfigValidateCommand(
    command_harness_config.CommandConfigBaseTestHarness
):
  """Test the ConfigVersionCommand class."""

  __test__ = True
  test_class: Type[config_version.ConfigVersionCommand]
  instance: config_version.ConfigVersionCommand

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = config_version.ConfigVersionCommand

  def invoke_command(self, config_file: Optional[str]) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_config = self.create_instance(config_file=config_file)
      m_click = stack.enter_context(patch(config_version.__name__ + ".click"))
      self.instance.invoke()
    return (
        m_click,
        m_config,
        m_config.return_value.get_config_file_name(),
        m_config.return_value.parse.return_value.version,
    )

  def test_invoke_default(self) -> None:
    m_click, m_config, path, version = self.invoke_command(config_file=None)
    m_config.return_value.parse.assert_called_once_with()
    m_config.assert_called_once_with(config_file=None)
    m_click.echo.assert_called_once_with(
        f"Configuration file: {path}\nConfiguration version: {version}"
    )

  def test_invoke_with_config(self) -> None:
    m_click, m_config, path, version = self.invoke_command(
        config_file=self.mock_config_file
    )
    m_config.return_value.parse.assert_called_once_with()
    m_config.assert_called_once_with(config_file=self.mock_config_file)
    m_click.echo.assert_called_once_with(
        f"Configuration file: {path}\nConfiguration version: {version}"
    )
