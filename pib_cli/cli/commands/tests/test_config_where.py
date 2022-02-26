"""Test the ConfigWhereCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

from pib_cli import config_filename

from .. import config_where
from ..bases.fixtures import command_harness


class TestConfigWhereCommand(command_harness.CommandBaseTestHarness):
  """Test the ConfigWhereCommand class."""

  __test__ = True
  test_class = config_where.ConfigWhereCommand
  instance: config_where.ConfigWhereCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_click = stack.enter_context(patch(config_where.__name__ + ".click"))
      self.instance.invoke()
    return (m_click,)

  def test_invoke(self) -> None:
    m_click = self.invoke_command()[0]
    m_click.echo.assert_called_once_with(
        f"Current Configuration: {config_filename}"
    )
