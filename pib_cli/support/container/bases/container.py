"""DevContainerBase class."""

import os
from pathlib import Path

from pib_cli.support.mixins import text_file


class DevContainerBase(text_file.TextFileReader):
  """Base class for development container classes."""

  file_container_marker = os.path.join("/", "etc", "container_release")
  file_version_marker = os.path.join("/", "etc", "container_pib_version")
  local_executable_folder = str((Path.home() / ".local/bin").resolve())
  minimum_pib_version = "1.0.0"
