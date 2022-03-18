"""Tests for the DevContainerException class."""

from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.support.container import exceptions


class DevContainerExceptionTest(TestCase):
  """Tests for the DevContainerException class."""

  def setUp(self) -> None:
    self.message = "Test Exception"
    self.exit_code = 0
    self.instance = exceptions.DevContainerException(
        self.message, exit_code=self.exit_code
    )

  def test_class_hierarchy(self) -> None:
    self.assertIsInstance(self.instance, BaseException)

  def test_initialization(self) -> None:
    self.assertEqual(self.instance.exit_code, self.exit_code)

  @patch(exceptions.__name__ + ".sys.exit")
  def test_exit(self, m_exit: Mock) -> None:
    self.instance.exit()
    m_exit.assert_called_once_with(self.exit_code)
