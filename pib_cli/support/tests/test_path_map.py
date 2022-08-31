"""Test the PathMap class."""

import os
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import Mock, patch

import git
from pib_cli import config
from pib_cli.config import yaml_keys
from pib_cli.support import path_map


@patch.dict(
    os.environ,
    {config.ENV_OVERRIDE_PROJECT_NAME: "test_name"},
    clear=True,
)
class TestPathMap:
  """Test the PathMap class."""

  class TestInit:
    """Tests for initialization of the PathMap class."""

    def test__init__throws_no_exception(self) -> None:
      path_map.PathMap()

  class TestRepoRootPath:
    """Tests for the repo_root_path property of the PathMap class."""

    mock_project_name = "test_name"
    mock_git_root_str = "/app"

    def test__returns_expected(self) -> None:
      instance = path_map.PathMap()
      with patch(path_map.__name__ + ".git.Repo") as m_git:
        m_git.return_value.working_tree_dir = self.mock_git_root_str

        result = instance.repo_root_path

      assert result == Path(self.mock_git_root_str)

    def test__is_cached(self) -> None:
      instance = path_map.PathMap()
      with patch(path_map.__name__ + ".git.Repo") as m_git:
        m_git.return_value.working_tree_dir = self.mock_git_root_str

        return_result_a = instance.repo_root_path
        return_result_b = instance.repo_root_path

      assert return_result_a == return_result_b
      m_git.assert_called_once_with(
          '.',
          search_parent_directories=True,
      )

    def test__instantiates_repo_as_expected(self) -> None:
      instance = path_map.PathMap()
      with patch(path_map.__name__ + ".git.Repo") as m_git:
        m_git.return_value.working_tree_dir = self.mock_git_root_str

        _ = instance.repo_root_path

      m_git.assert_called_once_with(
          '.',
          search_parent_directories=True,
      )

    def test__when_bare_repository__exits_with_msg(self) -> None:
      instance = path_map.PathMap()
      with ExitStack() as exit_stack:
        m_echo = exit_stack.enter_context(
            patch(path_map.__name__ + ".click.echo")
        )
        m_exit = exit_stack.enter_context(
            patch(path_map.__name__ + ".sys.exit")
        )
        m_git = exit_stack.enter_context(
            patch(path_map.__name__ + ".git.Repo"),
        )
        m_git.return_value.working_tree_dir = None

        _ = instance.repo_root_path

      m_exit.assert_called_once_with(config.EXIT_CODE_NOT_A_REPOSITORY)
      m_echo.assert_called_once_with("No git repository not found.")

    def test__when_no_repository__exits_with_msg(self) -> None:
      instance = path_map.PathMap()
      with ExitStack() as exit_stack:
        m_echo = exit_stack.enter_context(
            patch(path_map.__name__ + ".click.echo")
        )
        m_exit = exit_stack.enter_context(
            patch(path_map.__name__ + ".sys.exit")
        )
        m_git = exit_stack.enter_context(
            patch(path_map.__name__ + ".git.Repo"),
        )
        m_git.side_effect = git.InvalidGitRepositoryError

        _ = instance.repo_root_path

      m_exit.assert_called_once_with(config.EXIT_CODE_NOT_A_REPOSITORY)
      m_echo.assert_called_once_with("No git repository not found.")

  class TestDocumentationRootPath:
    """Tests for the documentation_root_path property of the PathMap class."""

    mock_git_root_path = Path("/app")
    mock_documentation_root_path = Path("documentation")

    @patch(path_map.__name__ + ".state.State")
    @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=True))
    def test__when_exists__returns_expected(self, m_state: Mock) -> None:
      instance = path_map.PathMap()
      with patch.object(
          instance,
          "_repo_root_path",
          self.mock_git_root_path,
      ):
        m_state.return_value.user_config.get_documentation_root.\
          return_value = self.mock_documentation_root_path

        result = instance.documentation_root_path

      assert result == \
        self.mock_git_root_path / self.mock_documentation_root_path

    @patch(path_map.__name__ + ".state.State")
    @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=True))
    def test__when_exists__is_cached(self, m_state: Mock) -> None:

      instance = path_map.PathMap()
      with patch.object(
          instance,
          "_repo_root_path",
          self.mock_git_root_path,
      ):
        m_get_documentation_root = (
            m_state.return_value.user_config.get_documentation_root
        )
        m_get_documentation_root.return_value = \
          self.mock_documentation_root_path

        return_result_a = instance.documentation_root_path
        return_result_b = instance.documentation_root_path

      assert return_result_a == return_result_b
      m_get_documentation_root.assert_called_once_with()

    @patch(path_map.__name__ + ".state.State")
    @patch(path_map.__name__ + ".sys.exit")
    @patch(path_map.__name__ + ".click.echo")
    @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=False))
    def test__when_does_not_exist__exits_with_msg(
        self,
        m_click: Mock,
        m_exit: Mock,
        m_state: Mock,
    ) -> None:
      instance = path_map.PathMap()
      with patch.object(
          instance,
          "_repo_root_path",
          self.mock_git_root_path,
      ):
        m_state.return_value.user_config.get_documentation_root.return_value = \
          self.mock_documentation_root_path

        _ = instance.documentation_root_path

        mock_path = Path(
            self.mock_git_root_path / self.mock_documentation_root_path
        )
        m_click.assert_called_once_with(
            f"ERROR: Documentation not found: {mock_path} "
            f"(config: {yaml_keys.V210_CLI_CONFIG_DOCS_FOLDER}, "
            f"env: {config.ENV_OVERRIDE_DOCUMENTATION_ROOT})"
        )
        m_exit.assert_called_once_with(
            config.EXIT_CODE_DOCUMENTATION_ROOT_NOT_FOUND
        )

  class TestProjectRootPath:
    """Tests for the project_root_path property of the PathMap class."""

    mock_git_root_path = Path("/app")
    mock_project_name = "test_name"

    @patch(path_map.__name__ + ".state.State")
    @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=True))
    def test__when_exists__returns_expected(self, m_state: Mock) -> None:
      instance = path_map.PathMap()
      with patch.object(
          instance,
          "_repo_root_path",
          self.mock_git_root_path,
      ):
        m_state.return_value.user_config.get_project_name.return_value = \
          self.mock_project_name

        result = instance.project_root_path

      assert result == self.mock_git_root_path / Path(self.mock_project_name)

    @patch(path_map.__name__ + ".state.State")
    @patch(path_map.__name__ + ".os.path.exists")
    def test__when_exists__is_cached(
        self,
        m_exists: Mock,
        m_state: Mock,
    ) -> None:
      instance = path_map.PathMap()
      m_exists.return_value = True
      with patch.object(
          instance,
          "_repo_root_path",
          self.mock_git_root_path,
      ):
        m_state.return_value.user_config.get_project_name.return_value = \
          self.mock_project_name

        return_result_a = instance.project_root_path
        return_result_b = instance.project_root_path

      mock_path = Path(self.mock_git_root_path / Path(self.mock_project_name))
      assert return_result_a == return_result_b
      m_exists.assert_called_once_with(mock_path)

    @patch(path_map.__name__ + ".state.State")
    @patch(path_map.__name__ + ".sys.exit")
    @patch(path_map.__name__ + ".click.echo")
    @patch(path_map.__name__ + ".os.path.exists", Mock(return_value=False))
    def test__when_does_not_exist__exits_with_msg(
        self,
        m_click: Mock,
        m_exit: Mock,
        m_state: Mock,
    ) -> None:
      instance = path_map.PathMap()
      with patch.object(
          instance,
          "_repo_root_path",
          self.mock_git_root_path,
      ):
        m_state.return_value.user_config.get_project_name.return_value = \
          self.mock_project_name

        _ = instance.project_root_path

      mock_path = Path(self.mock_git_root_path / Path(self.mock_project_name))
      m_click.assert_called_once_with(
          f"ERROR: Project not found: {mock_path} "
          f"(config: {yaml_keys.V210_CLI_CONFIG_PROJECT_NAME}, "
          f"env: {config.ENV_OVERRIDE_PROJECT_NAME})"
      )
      m_exit.assert_called_once_with(
          config.EXIT_CODE_PROJECT_NAME_ROOT_NOT_FOUND
      )

  class TestDocumentationRoot:
    """Tests for the documentation_root method of the PathMap class."""

    @patch(path_map.__name__ + ".os.chdir")
    def test__calls_chdir_correctly(self, mock_chdir: Mock) -> None:
      instance = path_map.PathMap()
      with patch.object(instance, "_documentation_root_path") as m_method:

        instance.documentation_root()

      mock_chdir.assert_called_once_with(m_method)

  class TestRepoRoot:
    """Tests for the repo_root method of the PathMap class."""

    @patch(path_map.__name__ + ".os.chdir")
    def test__calls_chdir_correctly(self, mock_chdir: Mock) -> None:
      instance = path_map.PathMap()
      with patch.object(instance, "_repo_root_path") as m_method:

        instance.repo_root()

      mock_chdir.assert_called_once_with(m_method)

  class TestGitRoot:
    """Tests for the git_root method of the PathMap class."""

    @patch(path_map.__name__ + ".os.chdir")
    def test__calls_chdir_correctly(self, mock_chdir: Mock) -> None:
      instance = path_map.PathMap()
      with patch.object(instance, "_repo_root_path") as m_method:

        instance.git_root()

      mock_chdir.assert_called_once_with(m_method)

  class TestProjectRoot:
    """Tests for the project_root method of the PathMap class."""

    @patch(path_map.__name__ + ".os.chdir")
    def test__calls_chdir_correctly(self, mock_chdir: Mock) -> None:
      instance = path_map.PathMap()
      with patch.object(instance, "_project_root_path") as m_method:

        instance.project_root()

      mock_chdir.assert_called_once_with(m_method)
