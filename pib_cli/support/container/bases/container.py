"""DevContainerBase class."""

import os
from pathlib import Path

from pib_cli import config
from pib_cli.support.mixins import text_file


class DevContainerBase(text_file.TextFileReader):
  """Base class for development container classes."""

  file_container_marker = os.path.join("/", "etc", "container_release")
  file_version_marker = os.path.join("/", "etc", "container_pib_version")
  local_executable_folder = str((Path.home() / ".local/bin").resolve())
  minimum_pib_version = "1.0.0"
  unversioned_pib_value = "0.0.1"
  incompatible_container_exit_code = config.EXIT_CODE_CONTAINER_INCOMPATIBLE
