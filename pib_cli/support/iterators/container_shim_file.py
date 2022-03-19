"""ContainerBashFileIterator for PIB CLI."""

import os
from pathlib import Path

import pib_cli
from pib_cli.support import container

from .bases import file_copy_base


class ContainerShimFileIterator(file_copy_base.FileCopyIteratorBase):
  """A iterator for the installation a CLI shim file.

  Creates a sequence of
  :class:`.SourceDestinationPair`
  to assist in the configuration of a PIB Development Container.
  """

  glob_pattern = os.path.join(Path(pib_cli.__file__).parent, "bash", "shim")

  def hook_create_destination(self, current_source: str) -> str:
    """Generate a home folder destination from a source file.

    :param current_source: The path to the source file.
    :returns: The new location of the shim file.
    """

    return os.path.join(container.DevContainer.local_executable_folder, 'dev')
