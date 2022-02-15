"""Test the PathMap class."""

import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli import config
from pib_cli.support import path_map


class TestPathMap(TestCase):
  """Test the PathMap class."""

  @patch.dict(os.environ, {config.ENV_PROJECT_NAME: "test_name"}, clear=True)
  def setUp(self) -> None:
    self.mock_project_name = "test_name"
    self.mock_root = "/app"
    with patch(path_map.__name__ + ".git.Repo") as m_git:
      m_git.return_value.working_tree_dir = Path("/app")
      self.path_manager = path_map.PathMap()
    self.mock_git_call = m_git

  def test_initialization_git_call(self) -> None:
    self.mock_git_call.assert_called_once_with(
        '.',
        search_parent_directories=True,
    )

  def test_initialization_instance_variables(self) -> None:
    self.assertEqual(self.path_manager.root, self.mock_root)
    self.assertEqual(
        self.path_manager.home,
        os.path.join(
            self.mock_root,
            self.mock_project_name,
        ),
    )
    self.assertEqual(
        self.path_manager.docs,
        os.path.join(
            self.mock_root,
            config.SETTING_DOCUMENTATION_FOLDER_NAME,
        ),
    )

  @patch(path_map.__name__ + ".os.chdir")
  def test_project_root(self, mock_chdir: Mock) -> None:
    self.path_manager.project_root()
    mock_chdir.assert_called_once_with(self.path_manager.root)

  @patch(path_map.__name__ + ".os.chdir")
  def test_project_home(self, mock_chdir: Mock) -> None:
    self.path_manager.project_home()
    mock_chdir.assert_called_once_with(self.path_manager.home)

  @patch(path_map.__name__ + ".os.chdir")
  def test_project_docs(self, mock_chdir: Mock) -> None:
    self.path_manager.project_docs()
    mock_chdir.assert_called_once_with(self.path_manager.docs)
