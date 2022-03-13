"""Test the ConfigShowCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

from .. import config_show
from ..bases.fixtures import command_harness


class TestConfigShow(command_harness.CommandBaseTestHarness):
  """Test the ConfigShowCommand class."""

  __test__ = True
  test_class = config_show.ConfigShowCommand
  instance: config_show.ConfigShowCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_click = stack.enter_context(patch(config_show.__name__ + ".click"))
      m_state = stack.enter_context(
          patch(config_show.__name__ + ".state.State")
      )
      m_state.return_value.user_config.get_raw_file.return_value = (
          "mock config data "
      )
      self.instance.invoke()
    return m_click, m_state

  def test_invoke(self) -> None:
    m_click, m_state = self.invoke_command()
    m_click.echo.assert_called_once_with(
        m_state.return_value.user_config.get_raw_file.return_value
    )
