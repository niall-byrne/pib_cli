"""CLI External Command Management Class"""

import glob
import os
import shutil
from pathlib import Path

from .. import config, project_root
from .container import ContainerManager


def setup_bash():
  if not ContainerManager.is_container():
    return config.ERROR_CONTAINER_ONLY
  results = []
  bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
  home_dir = str(Path.home())
  for file_name in bash_files:
    shutil.copy(file_name, home_dir)
    results.append(f"Copied: {file_name} -> {home_dir} ")
  results.append(config.SETTING_BASH_SETUP_SUCCESS_MESSAGE)
  return "\n".join(results)
