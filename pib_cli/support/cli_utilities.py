"""CLI Utilities"""

from .paths import PathManager
from .processes import ProcessManager


class Utilities:

  def __init__(self):
    self.process_manager = ProcessManager()
    self.path_manager = PathManager()
