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
      m_state = stack.enter_context(
          patch(config_validate.__name__ + ".state.State")
      )
      self.instance.invoke()
    return m_click, m_state

  def test_invoke(self) -> None:
    m_click, m_state = self.invoke_command()
    m_state.return_value.user_config.validate.assert_called_once_with()
    m_click.echo.assert_called_once_with("Current configuration is valid.")
