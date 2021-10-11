"""Path Management Classes."""

import abc
import os

from .. import config
from .dev_container import DevContainer


def get_path_manager():
  """Return the appropriate BasePathManager implementation."""

  if DevContainer.is_container():
    return DevContainerPathManager()
  return ExternalPathManager()


class BasePathManager(abc.ABC):
  """The Path Manager Interface."""

  @abc.abstractmethod
  def project_root(self):
    """Abstract project_root method."""

  @abc.abstractmethod
  def project_home(self):
    """Abstract project_home method."""

  @abc.abstractmethod
  def project_docs(self):
    """Abstract project_docs method."""


class DevContainerPathManager(BasePathManager):
  """Manages changing location inside a dev container."""

  def __init__(self):
    self.root = os.path.join("/", config.SETTING_PROJECT_ROOT_NAME)
    self.home = os.path.join(
        self.root,
        os.environ.get(config.ENV_PROJECT_NAME, None),
    )
    self.docs = os.path.join(
        self.root,
        config.SETTING_DOCUMENTATION_FOLDER_NAME,
    )

  def project_root(self):
    """Change the path to the project root folder location."""
    os.chdir(self.root)

  def project_home(self):
    """Change the path to the project home folder location."""
    os.chdir(self.home)

  def project_docs(self):
    """Change the path to the project documentation location."""
    os.chdir(self.docs)


class ExternalPathManager(BasePathManager):
  """Manages changing location on the local file-system."""

  def __init__(self):

    self.root = "."
    self.home = os.environ.get(config.ENV_PROJECT_NAME, None)
    self.docs = config.SETTING_DOCUMENTATION_FOLDER_NAME

  def __git_root(self):
    if os.path.exists(".git"):
      return
    os.chdir("..")
    self.__git_root()

  def project_root(self):
    """Change the path to the project root folder location."""
    self.__git_root()

  def project_home(self):
    """Change the path to the project home folder location."""
    self.__git_root()
    os.chdir(self.home)

  def project_docs(self):
    """Change the path to the project documentation location."""
    self.__git_root()
    os.chdir(self.docs)
