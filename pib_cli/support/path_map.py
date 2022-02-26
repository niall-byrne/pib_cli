"""PathMap class."""

import os

import git
from pib_cli import config


class PathMap:
  """Path mappings for a PIB git repository."""

  def __init__(self) -> None:
    self.git_root_folder = str(
        git.Repo(
            os.curdir,
            search_parent_directories=True,
        ).working_tree_dir
    )
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

  def documentation_root(self) -> None:
    """Change the path to the project documentation folder location."""

    os.chdir(self.documentation_root_folder)

  def git_root(self) -> None:
    """Change the path to the git root folder location."""

    os.chdir(self.git_root_folder)

  def project_root(self) -> None:
    """Change the path to the project's codebase root folder location."""

    os.chdir(self.project_root_folder)
