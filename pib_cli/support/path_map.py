"""PathMap class."""

import os
import pathlib
import sys

import click
import git
from pib_cli import config
from pib_cli.config.locale import _


class PathMap:
  """Path mappings for a PIB git repository."""

  def __init__(self) -> None:
    self.git_root_folder = self._get_repository_root()
    self.documentation_root_folder = os.path.join(
        self.git_root_folder,
        config.DOCUMENTATION_FOLDER_NAME,
    )
    self.project_root_folder = os.path.join(
        self.git_root_folder,
        os.environ.get(
            config.ENV_PROJECT_NAME,
            "not-defined",
        ),
    )

  def _get_repository_root(self) -> pathlib.Path:
    try:
      return self._get_repository_root_as_path()
    except git.InvalidGitRepositoryError:
      click.echo(_("No git repository not found."))
      sys.exit(config.EXIT_CODE_NOT_A_REPOSITORY)

  def _get_repository_root_as_path(self) -> pathlib.Path:
    root = git.Repo(
        os.curdir,
        search_parent_directories=True,
    ).working_tree_dir
    if root:
      return pathlib.Path(root).absolute()
    return pathlib.Path(os.curdir).absolute()

  def documentation_root(self) -> None:
    """Change the path to the project documentation folder location."""

    os.chdir(self.documentation_root_folder)

  def git_root(self) -> None:
    """Change the path to the git root folder location."""

    os.chdir(self.git_root_folder)

  def project_root(self) -> None:
    """Change the path to the project's codebase root folder location."""

    os.chdir(self.project_root_folder)
