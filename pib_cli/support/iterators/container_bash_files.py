"""ContainerBashFilesIterator class."""

import os
from pathlib import Path

import pib_cli

from .bases import file_copy_base


class ContainerBashFilesIterator(file_copy_base.FileCopyIteratorBase):
  """A iterator for the installation of BASH configuration.

  Creates a sequence of
  :class:`.SourceDestinationPair`
  to assist in the configuration of a PIB Development Container.
  """

  glob_pattern = os.path.join(Path(pib_cli.__file__).parent, "bash", "bash*")

  def hook_create_destination(self, current_source: str) -> str:
    """Generate a home folder destination from a source file.

    :param current_source: The path to the source file.
    :returns: The new location of the source file in the home folder.
    """

    destination_base_name = "." + str(Path(current_source).name)
    return str((Path.home() / destination_base_name).resolve())
