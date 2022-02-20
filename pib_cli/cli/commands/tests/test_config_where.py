"""Test the ConfigWhereCommand class."""

from unittest.mock import Mock, patch

from pib_cli import config_filename

from .. import config_where
from ..bases.fixtures import command_harness


class TestConfigWhereCommand(command_harness.CommandBaseTestHarness):
  """Test the ConfigWhereCommand class."""

  __test__ = True
  test_class = config_where.ConfigWhereCommand

  @patch(config_where.__name__ + ".click")
  def test_invoke(self, m_module: Mock) -> None:

    self.instance.invoke()

    m_module.echo.assert_called_once_with(
        f"Current Configuration: {config_filename}"
    )
