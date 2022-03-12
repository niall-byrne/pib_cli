"""Test the handler function."""

from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.cli import commands

from .. import handler


class TestHandler(TestCase):
  """The the handler function."""

  def setUp(self) -> None:
    self.mock_command = Mock()
    self.mock_config_file = "./config.yml"

  def test_handler_base_command(self) -> None:
    with patch(commands.__name__ + ".issubclass") as m_issubclass:
      m_issubclass.return_value = False
      handler(self.mock_command)

    self.mock_command.assert_called_once_with()
    self.mock_command.return_value.invoke.assert_called_once_with()

  def test_handler_config_command_defaults(self) -> None:
    with patch(commands.__name__ + ".issubclass") as m_issubclass:
      m_issubclass.return_value = True
      handler(self.mock_command)

    self.mock_command.assert_called_once_with(config_file=None)
    self.mock_command.return_value.invoke.assert_called_once_with()

  def test_handler_config_command_args(self) -> None:
    with patch(commands.__name__ + ".issubclass") as m_issubclass:
      m_issubclass.return_value = True
      handler(self.mock_command, config_file=self.mock_config_file)

    self.mock_command.assert_called_once_with(config_file=self.mock_config_file)
    self.mock_command.return_value.invoke.assert_called_once_with()
