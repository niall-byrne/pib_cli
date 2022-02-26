"""Test the ConfigValidateCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

from .. import config_validate
from ..bases.fixtures import command_harness


class TestConfigValidateCommand(command_harness.CommandBaseTestHarness):
  """Test the ConfigValidateCommand class."""

  __test__ = True
  test_class = config_validate.ConfigValidateCommand
  instance: config_validate.ConfigValidateCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_click = stack.enter_context(patch(config_validate.__name__ + ".click"))
      m_config = stack.enter_context(
          patch(
              config_validate.__name__ + ".user_configuration.UserConfiguration"
          )
      )
      self.instance.invoke()
    return m_click, m_config

  def test_invoke(self) -> None:
    m_click, m_config = self.invoke_command()
    m_config.return_value.validate.assert_called_once_with()
    m_click.echo.assert_called_once_with("Current configuration is valid.")
