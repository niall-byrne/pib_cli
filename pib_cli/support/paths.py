"""Paths Manager"""

import os


class PathManager:

  def __init__(self):
    self.root = '/app'
    self.home = os.path.join('/app', os.environ.get("PROJECT_NAME", None))
    self.docs = os.path.join('/app', "documentation")
    self.container_marker = os.path.join("/", "etc", "container_release")

  def is_container(self):
    return os.path.exists(self.container_marker)

  def project_root(self):
    os.chdir(self.root)

  def project_home(self):
    os.chdir(self.home)

  def project_docs(self):
    os.chdir(self.docs)
