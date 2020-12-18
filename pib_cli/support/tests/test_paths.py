"""Test the Path Manager"""

import os
from unittest import TestCase
from unittest.mock import patch

from pib_cli.support.paths import PathManager


class TestPathManager(TestCase):

  def setUp(self):
    self.path_manager = PathManager()

  def test_initial_instance_variables(self):
    assert self.path_manager.root == os.environ.get("PROJECT_ROOT")
    assert self.path_manager.home == os.path.join(
        self.path_manager.root, os.environ.get("PROJECT_NAME"))
    assert self.path_manager.docs == os.path.join(self.path_manager.root,
                                                  "documentation")

  @patch("pib_cli.support.paths.os.chdir")
  def test_project_root(self, mock_chdir):
    self.path_manager.project_root()
    mock_chdir.assert_called_once_with(self.path_manager.root)

  @patch("pib_cli.support.paths.os.chdir")
  def test_project_home(self, mock_chdir):
    self.path_manager.project_home()
    mock_chdir.assert_called_once_with(self.path_manager.home)

  @patch("pib_cli.support.paths.os.chdir")
  def test_project_docs(self, mock_chdir):
    self.path_manager.project_docs()
    mock_chdir.assert_called_once_with(self.path_manager.docs)
