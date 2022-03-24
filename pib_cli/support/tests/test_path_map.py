"""Test the PathMap class."""

import os
from contextlib import ExitStack
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

import git
from pib_cli import config
from pib_cli.config import yaml_keys
from pib_cli.support import path_map


class TestPathMap(TestCase):
  """Test the PathMap class."""

  instance: path_map.PathMap

  def create_instance(self) -> None:
    self.path_manager = path_map.PathMap()

  @patch.dict(
      os.environ,
      {config.ENV_OVERRIDE_PROJECT_NAME: "test_name"},
      clear=True,
  )
  def setUp(self) -> None:
    self.mock_project_name = "test_name"
    self.mock_git_root_str = "/app"
    self.mock_git_root_path = Path(self.mock_git_root_str)
    self.mock_documentation_root_path = Path("documentation")
    self.mock_project_root_path = Path(self.mock_project_name)
    self.create_instance()

  def test_repo_root_path(self) -> None:
    with patch(path_map.__name__ + ".git.Repo") as m_git:
      m_git.return_value.working_tree_dir = self.mock_git_root_str
      result = self.path_manager.repo_root_path
      m_git.assert_called_once_with(
          '.',
          search_parent_directories=True,
      )
      self.assertEqual(result, self.mock_git_root_path)

  def test_repo_root_path_cached(self) -> None:
    with patch(path_map.__name__ + ".git.Repo") as m_git:
      m_git.return_value.working_tree_dir = self.mock_git_root_str
      _ = self.path_manager.repo_root_path
      _ = self.path_manager.repo_root_path
    m_git.assert_called_once_with(
        '.',
        search_parent_directories=True,
    )

  def test_repo_root_path_bare_repository(self) -> None:
    with ExitStack() as exit_stack:
      m_echo = exit_stack.enter_context(
          patch(path_map.__name__ + ".click.echo")
      )
      m_exit = exit_stack.enter_context(patch(path_map.__name__ + ".sys.exit"))
      m_git = exit_stack.enter_context(patch(path_map.__name__ + ".git.Repo"),)

      m_git.return_value.working_tree_dir = None
      _ = self.path_manager.repo_root_path
      m_git.assert_called_once_with(
          '.',
          search_parent_directories=True,
      )
      m_exit.assert_called_once_with(config.EXIT_CODE_NOT_A_REPOSITORY)
      m_echo.assert_called_once_with("No git repository not found.")

  def test_repo_root_path_no_repository(self) -> None:
    with ExitStack() as exit_stack:
      m_echo = exit_stack.enter_context(
          patch(path_map.__name__ + ".click.echo")
      )
      m_exit = exit_stack.enter_context(patch(path_map.__name__ + ".sys.exit"))
      m_git = exit_stack.enter_context(patch(path_map.__name__ + ".git.Repo"),)

      m_git.side_effect = git.InvalidGitRepositoryError
      _ = self.path_manager.repo_root_path
      m_git.assert_called_once_with(
          '.',
          search_parent_directories=True,
      )
      m_exit.assert_called_once_with(config.EXIT_CODE_NOT_A_REPOSITORY)
      m_echo.assert_called_once_with("No git repository not found.")

  @patch(path_map.__name__ + ".state.State")
  @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=True))
  def test_documentation_root_path(self, m_state: Mock) -> None:
    with patch.object(
        self.path_manager,
        "_repo_root_path",
        self.mock_git_root_path,
    ):
      m_state.return_value.user_config.get_documentation_root.return_value = \
        self.mock_documentation_root_path

      result = self.path_manager.documentation_root_path

      self.assertEqual(
          result,
          Path(self.mock_git_root_str / self.mock_documentation_root_path)
      )

  @patch(path_map.__name__ + ".state.State")
  @patch(path_map.__name__ + ".sys.exit")
  @patch(path_map.__name__ + ".click.echo")
  @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=False))
  def test_documentation_root_path_does_not_exist(
      self,
      m_click: Mock,
      m_exit: Mock,
      m_state: Mock,
  ) -> None:
    with patch.object(
        self.path_manager,
        "_repo_root_path",
        self.mock_git_root_path,
    ):
      m_state.return_value.user_config.get_documentation_root.return_value = \
        self.mock_documentation_root_path

      _ = self.path_manager.documentation_root_path
      mock_path = Path(
          self.mock_git_root_str / self.mock_documentation_root_path
      )

      m_click.assert_called_once_with(
          f"ERROR: Documentation not found: {mock_path} "
          f"(config: {yaml_keys.V210_CLI_CONFIG_DOCS_FOLDER}, "
          f"env: {config.ENV_OVERRIDE_DOCUMENTATION_ROOT})"
      )
      m_exit.assert_called_once_with(
          config.EXIT_CODE_DOCUMENTATION_ROOT_NOT_FOUND
      )

  @patch(path_map.__name__ + ".state.State")
  @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=True))
  def test_project_root_path(self, m_state: Mock) -> None:
    with patch.object(
        self.path_manager,
        "_repo_root_path",
        self.mock_git_root_path,
    ):
      m_state.return_value.user_config.get_project_name.return_value = \
        self.mock_project_name

      result = self.path_manager.project_root_path

      self.assertEqual(
          result, Path(self.mock_git_root_str / self.mock_project_root_path)
      )

  @patch(path_map.__name__ + ".state.State")
  @patch(path_map.__name__ + ".sys.exit")
  @patch(path_map.__name__ + ".click.echo")
  @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=False))
  def test_project_root_path_does_not_exist(
      self,
      m_click: Mock,
      m_exit: Mock,
      m_state: Mock,
  ) -> None:
    with patch.object(
        self.path_manager,
        "_repo_root_path",
        self.mock_git_root_path,
    ):
      m_state.return_value.user_config.get_project_name.return_value = \
        self.mock_project_name

      _ = self.path_manager.project_root_path
      mock_path = Path(self.mock_git_root_str / self.mock_project_root_path)

      m_click.assert_called_once_with(
          f"ERROR: Project not found: {mock_path} "
          f"(config: {yaml_keys.V210_CLI_CONFIG_PROJECT_NAME}, "
          f"env: {config.ENV_OVERRIDE_PROJECT_NAME})"
      )
      m_exit.assert_called_once_with(
          config.EXIT_CODE_PROJECT_NAME_ROOT_NOT_FOUND
      )

  @patch(path_map.__name__ + ".os.chdir")
  def test_git_root(self, mock_chdir: Mock) -> None:
    with patch.object(self.path_manager, "_repo_root_path") as m_method:
      self.path_manager.git_root()
    mock_chdir.assert_called_once_with(m_method)

  @patch(path_map.__name__ + ".os.chdir")
  def test_project_root(self, mock_chdir: Mock) -> None:
    with patch.object(self.path_manager, "_project_root_path") as m_method:
      self.path_manager.project_root()
    mock_chdir.assert_called_once_with(m_method)

  @patch(path_map.__name__ + ".os.chdir")
  def test_documentation_root(self, mock_chdir: Mock) -> None:
    with patch.object(
        self.path_manager, "_documentation_root_path"
    ) as m_method:
      self.path_manager.documentation_root()
    mock_chdir.assert_called_once_with(m_method)
