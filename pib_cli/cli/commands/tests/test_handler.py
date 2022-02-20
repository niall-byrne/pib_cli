"""Test the handler function."""

from unittest import TestCase
from unittest.mock import Mock

from .. import handler


class TestHandler(TestCase):
  """The the handler function."""

  def setUp(self) -> None:
    self.mock_command = Mock()

  def test_handler(self) -> None:
    handler(self.mock_command)

    self.mock_command.assert_called_once_with()
    self.mock_command.return_value.invoke.assert_called_once_with()
