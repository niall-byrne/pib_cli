"""Test the ConfigValidateCommand class."""

from unittest.mock import Mock, patch

from .. import config_validate
from ..bases.fixtures import command_harness


class TestConfigValidateCommand(command_harness.CommandBaseTestHarness):
  """Test the ConfigValidateCommand class."""

  __test__ = True
  test_class = config_validate.ConfigValidateCommand

  @patch(config_validate.__name__ + ".click")
  def test_invoke(self, m_module: Mock) -> None:

    with patch(
        config_validate.__name__ + ".user_configuration.UserConfiguration"
    ) as m_validator:
      self.instance.invoke()

    m_validator.return_value.validate.assert_called_once_with()
    m_module.echo.assert_called_once_with("Current configuration is valid.")
