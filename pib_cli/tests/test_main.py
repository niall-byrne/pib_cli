"""Test the main module."""

from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli import main


class TestMain(TestCase):
  """Test the main function."""

  @patch(main.__name__ + ".cli_interface")
  def test_main(self, m_cli: Mock) -> None:
    main.main()
    m_cli.assert_called_once_with()
