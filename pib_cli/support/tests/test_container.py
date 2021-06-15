"""Tests for the Container Manager Class."""

from unittest import TestCase
from unittest.mock import patch

from ... import config, patchbay
from ..container import Container


class TestContainerClass(TestCase):
  """Test the Container class."""

  @patch(patchbay.CONTAINER_MANAGER_OS_PATH_EXISTS)
  def test_is_container_true(self, mock_exists):
    mock_exists.return_value = True
    result = Container.is_container()
    mock_exists.assert_called_once_with(config.SETTING_CONTAINER_MARKER)
    self.assertTrue(result)

  @patch(patchbay.CONTAINER_MANAGER_OS_PATH_EXISTS)
  def test_is_container_false(self, mock_exists):
    mock_exists.return_value = False
    result = Container.is_container()
    mock_exists.assert_called_once_with(config.SETTING_CONTAINER_MARKER)
    self.assertFalse(result)
