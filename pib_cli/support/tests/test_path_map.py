"""Test the PathMap class."""

import os
from contextlib import ExitStack
from pathlib import Path
from typing import Optional, Union
from unittest import TestCase
from unittest.mock import Mock, patch

import git
from pib_cli import config
from pib_cli.support import path_map


class TestPathMap(TestCase):
  """Test the PathMap class."""

  instance: path_map.PathMap
  mock_git_call: Mock

  def create_instance(
      self, working_tree_dir: Union[git.InvalidGitRepositoryError,
                                    Optional[str]]
  ) -> None:
    with patch(path_map.__name__ + ".git.Repo") as m_git:
      if isinstance(working_tree_dir, git.InvalidGitRepositoryError):
        m_git.side_effect = working_tree_dir
      else:
        m_git.return_value.working_tree_dir = working_tree_dir
      self.path_manager = path_map.PathMap()
      self.mock_git_call = m_git

  @patch.dict(
      os.environ, {config.ENV_OVERRIDE_PROJECT_NAME: "test_name"}, clear=True
  )
  def setUp(self) -> None:
    self.mock_project_name = "test_name"
    self.mock_git_root_str = "/app"
    self.mock_git_root_path = Path(self.mock_git_root_str)
    self.create_instance(working_tree_dir=self.mock_git_root_str)

  def test_initialization_git_repo(self) -> None:
    self.mock_git_call.assert_called_once_with(
        '.',
        search_parent_directories=True,
    )
    self.assertEqual(self.path_manager.git_root_folder, self.mock_git_root_path)
    self.assertEqual(
        self.path_manager.documentation_root_folder,
        os.path.join(
            self.mock_git_root_path,
            config.DOCUMENTATION_FOLDER_NAME,
        ),
    )
    self.assertEqual(
        self.path_manager.project_root_folder,
        os.path.join(
            self.mock_git_root_path,
            self.mock_project_name,
        ),
    )

  def test_initialization_bare_git_repo(self) -> None:
    self.create_instance(working_tree_dir=None)
    self.mock_git_call.assert_called_once_with(
        '.',
        search_parent_directories=True,
    )
    self.assertEqual(
        self.path_manager.git_root_folder,
        Path(os.curdir).absolute()
    )

  def test_initialization_no_repo(self) -> None:
    with ExitStack() as exit_stack:
      exit_stack.enter_context(self.assertRaises(TypeError))
      m_echo = exit_stack.enter_context(
          patch(path_map.__name__ + ".click.echo")
      )
      m_exit = exit_stack.enter_context(patch(path_map.__name__ + ".sys.exit"))

      self.create_instance(
          working_tree_dir=git.
          InvalidGitRepositoryError("Not a git repository.")
      )
      m_exit.assert_called_once_with(config.EXIT_CODE_NOT_A_REPOSITORY)
      m_echo.assert_called_once_with("No git repository not found.")

  @patch(path_map.__name__ + ".os.chdir")
  def test_git_root(self, mock_chdir: Mock) -> None:
    self.path_manager.git_root()
    mock_chdir.assert_called_once_with(self.path_manager.git_root_folder)

  @patch(path_map.__name__ + ".os.chdir")
  def test_project_root(self, mock_chdir: Mock) -> None:
    self.path_manager.project_root()
    mock_chdir.assert_called_once_with(self.path_manager.project_root_folder)

  @patch(path_map.__name__ + ".os.chdir")
  def test_documentation_root(self, mock_chdir: Mock) -> None:
    self.path_manager.documentation_root()
    mock_chdir.assert_called_once_with(
        self.path_manager.documentation_root_folder
    )
