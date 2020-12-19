"""Test the Container Manager Class"""

from unittest import TestCase
from unittest.mock import patch

from ... import config, patchbay
from ..container import ContainerManager


class TestContainerClass(TestCase):

  @patch(patchbay.CONTAINER_MANAGER_OS_PATH_EXISTS)
  def test_is_container_true(self, mock_exists):
    mock_exists.return_value = True
    result = ContainerManager.is_container()
    mock_exists.assert_called_once_with(config.SETTING_CONTAINER_MARKER)
    self.assertTrue(result)

  @patch(patchbay.CONTAINER_MANAGER_OS_PATH_EXISTS)
  def test_is_container_false(self, mock_exists):
    mock_exists.return_value = False
    result = ContainerManager.is_container()
    mock_exists.assert_called_once_with(config.SETTING_CONTAINER_MARKER)
    self.assertFalse(result)
