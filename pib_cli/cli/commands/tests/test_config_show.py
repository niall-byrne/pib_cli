"""Test the ConfigShowCommand class."""

from unittest.mock import Mock, patch

from .. import config_show
from ..bases.fixtures import command_harness


class TestConfigShow(command_harness.CommandBaseTestHarness):
  """Test the ConfigShowCommand class."""

  __test__ = True
  test_class = config_show.ConfigShowCommand

  @patch(config_show.__name__ + ".click")
  def test_invoke(self, m_module: Mock) -> None:

    with patch(
        config_show.__name__ + ".user_configuration.UserConfiguration"
    ) as m_config:
      m_config.return_value.get_raw_file.return_value = "mock config data "
      self.instance.invoke()

    m_module.echo.assert_called_once_with(
        m_config.return_value.get_raw_file.return_value
    )
