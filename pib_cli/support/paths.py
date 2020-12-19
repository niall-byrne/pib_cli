"""Path Management Class"""

import os

from .. import config


class PathManager:

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
    os.chdir(self.root)

  def project_home(self):
    os.chdir(self.home)

  def project_docs(self):
    os.chdir(self.docs)
