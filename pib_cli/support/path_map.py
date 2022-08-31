"""PathMap class."""

import os
import pathlib
import sys
from typing import Optional

import click
import git
from pib_cli import config
from pib_cli.config import yaml_keys
from pib_cli.config.locale import _
from pib_cli.support import state


class PathMap:
  """Path mappings for a PIB git repository."""

  def __init__(self) -> None:
    self._repo_root_path: Optional[pathlib.Path] = None
    self._documentation_root_path: Optional[pathlib.Path] = None
    self._project_root_path: Optional[pathlib.Path] = None

  @property
  def repo_root_path(self) -> pathlib.Path:
    """Return the path to the repository's root folder."""

    if not self._repo_root_path:
      try:
        root = git.Repo(
            os.curdir,
            search_parent_directories=True,
        ).working_tree_dir
        if not root:
          raise git.InvalidGitRepositoryError
        pathlib.Path(root).absolute()
        self._repo_root_path = pathlib.Path(root).absolute()
      except git.InvalidGitRepositoryError:
        click.echo(_("No git repository not found."))
        sys.exit(config.EXIT_CODE_NOT_A_REPOSITORY)
    return self._repo_root_path

  @property
  def documentation_root_path(self) -> pathlib.Path:
    """Return the path to the documentation root."""

    if not self._documentation_root_path:
      documentation_relative_path = state.State().\
        user_config.get_documentation_root()
      documentation_absolute_path = (
          self.repo_root_path / documentation_relative_path
      )
      self._validate_path(
          documentation_absolute_path,
          _(
              "ERROR: Documentation not found: {path} "
              "(config: {key}, env: {env})"
          ).format(
              path=documentation_absolute_path,
              key=yaml_keys.V210_CLI_CONFIG_DOCS_FOLDER,
              env=config.ENV_OVERRIDE_DOCUMENTATION_ROOT,
          ),
          config.EXIT_CODE_DOCUMENTATION_ROOT_NOT_FOUND
      )
      self._documentation_root_path = documentation_absolute_path.absolute()
    return self._documentation_root_path

  @property
  def project_root_path(self) -> pathlib.Path:
    """Return the path to the project root."""

    if not self._project_root_path:
      project_relative_path = state.State().\
        user_config.get_project_name()
      project_absolute_path = self.repo_root_path / project_relative_path
      self._validate_path(
          project_absolute_path,
          _(
              "ERROR: Project not found: {path}"
              " (config: {key}, env: {env})"
          ).format(
              path=project_absolute_path,
              key=yaml_keys.V210_CLI_CONFIG_PROJECT_NAME,
              env=config.ENV_OVERRIDE_PROJECT_NAME,
          ),
          config.EXIT_CODE_PROJECT_NAME_ROOT_NOT_FOUND
      )
      self._project_root_path = project_absolute_path
    return self._project_root_path

  def _validate_path(
      self,
      path: pathlib.Path,
      message: str,
      exit_code: int,
  ) -> None:
    if not os.path.exists(path):
      click.echo(message)
      sys.exit(exit_code)

  def documentation_root(self) -> None:
    """Change the path to the project documentation folder location."""

    os.chdir(self.documentation_root_path)

  def repo_root(self) -> None:
    """Change the path to the repository root folder location."""

    os.chdir(self.repo_root_path)

  def project_root(self) -> None:
    """Change the path to the project's codebase root folder location."""

    os.chdir(self.project_root_path)

  def git_root(self) -> None:
    """Change the path to the repository root folder location.

    This is an alias of :func:`~.PathMap.repo_root`.
    """

    self.repo_root()
