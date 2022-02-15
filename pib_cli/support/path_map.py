"""PathMap class."""

import os

import git
from pib_cli import config


class PathMap:
  """Path mappings for a PIB git repository."""

  def __init__(self) -> None:
    self.root = str(
        git.Repo(
            os.curdir,
            search_parent_directories=True,
        ).working_tree_dir
    )
    self.home = os.path.join(
        self.root,
        os.environ.get(
            config.ENV_PROJECT_NAME,
            "not-defined",
        ),
    )
    self.docs = os.path.join(
        self.root,
        config.SETTING_DOCUMENTATION_FOLDER_NAME,
    )

  def project_root(self) -> None:
    """Change the path to the project root folder location."""
    os.chdir(self.root)

  def project_home(self) -> None:
    """Change the path to the project home folder location."""
    os.chdir(self.home)

  def project_docs(self) -> None:
    """Change the path to the project documentation folder location."""
    os.chdir(self.docs)
