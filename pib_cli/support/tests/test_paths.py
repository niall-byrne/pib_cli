"""Test the Path Manager"""

import os
from unittest import TestCase
from unittest.mock import call, patch

from ... import config, patchbay
from ..paths import (
    BasePathManager,
    ContainerPathManager,
    ExternalPathManager,
    get_path_manager,
)


class TestBasePathManager(TestCase):

  @patch.multiple(BasePathManager, __abstractmethods__=set())
  def setUp(self):
    # pylint: disable=abstract-class-instantiated
    self.path_manager = BasePathManager()

  def test_methods_present(self):
    self.path_manager.project_root()
    self.path_manager.project_home()
    self.path_manager.project_docs()


class TestGetPathManager(TestCase):

  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER, return_value=True)
  def test_is_container(self, _):
    path_manager = get_path_manager()
    self.assertIsInstance(path_manager, ContainerPathManager)

  @patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER, return_value=False)
  def test_is_not_container(self, _):
    path_manager = get_path_manager()
    self.assertIsInstance(path_manager, ExternalPathManager)


class TestContainerPathManager(TestCase):

  def setUp(self):
    self.path_manager = ContainerPathManager()

  def test_initial_instance_variables(self):
    assert self.path_manager.root == os.path.join(
        '/', config.SETTING_PROJECT_ROOT_NAME
    )
    assert self.path_manager.home == os.path.join(
        self.path_manager.root, os.environ.get(config.ENV_PROJECT_NAME)
    )
    assert self.path_manager.docs == os.path.join(
        self.path_manager.root, config.SETTING_DOCUMENTATION_FOLDER_NAME
    )

  @patch(patchbay.PATH_MANAGER_OS_CHDIR)
  def test_project_root_inside_container(self, mock_chdir):
    self.path_manager.project_root()
    mock_chdir.assert_called_once_with(self.path_manager.root)

  @patch(patchbay.PATH_MANAGER_OS_CHDIR)
  def test_project_home_inside_container(self, mock_chdir):
    self.path_manager.project_home()
    mock_chdir.assert_called_once_with(self.path_manager.home)

  @patch(patchbay.PATH_MANAGER_OS_CHDIR)
  def test_project_docs_inside_container(self, mock_chdir):
    self.path_manager.project_docs()
    mock_chdir.assert_called_once_with(self.path_manager.docs)


class TestExternalPathManager(TestCase):

  def setUp(self):
    self.path_manager = ExternalPathManager()

  def test_initial_instance_variables(self):
    assert self.path_manager.root == "."
    assert self.path_manager.home == os.environ.get("PROJECT_NAME")
    assert self.path_manager.docs == config.SETTING_DOCUMENTATION_FOLDER_NAME

  @patch(patchbay.PATH_MANAGER_OS_PATH_EXISTS)
  @patch(patchbay.PATH_MANAGER_OS_CHDIR)
  def test_project_root_outside_container(self, mock_chdir, mock_exists):
    root_search = (False, False, True)
    mock_exists.side_effect = root_search
    self.path_manager.project_root()
    self.assertEqual(mock_exists.call_count, len(root_search))
    self.assertEqual(mock_exists.call_count, len(root_search))
    mock_chdir.assert_has_calls([call(".."), call("..")])

  @patch(patchbay.PATH_MANAGER_OS_PATH_EXISTS)
  @patch(patchbay.PATH_MANAGER_OS_CHDIR)
  def test_project_home_outside_container(self, mock_chdir, mock_exists):
    root_search = (False, False, True)
    mock_exists.side_effect = root_search
    self.path_manager.project_home()
    self.assertEqual(mock_exists.call_count, len(root_search))
    self.assertEqual(mock_exists.call_count, len(root_search))
    mock_chdir.assert_has_calls([call(".."), call("..")])

  @patch(patchbay.PATH_MANAGER_OS_PATH_EXISTS)
  @patch(patchbay.PATH_MANAGER_OS_CHDIR)
  def test_project_docs_outside_container(self, mock_chdir, mock_exists):
    root_search = (False, False, True)
    mock_exists.side_effect = root_search
    self.path_manager.project_docs()
    self.assertEqual(mock_exists.call_count, len(root_search))
    self.assertEqual(mock_exists.call_count, len(root_search))
    mock_chdir.assert_has_calls([call(".."), call("..")])
