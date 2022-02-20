"""DevContainerInstaller class."""

import os
import shutil
from typing import Callable, List

from pib_cli.support import container
from pib_cli.support.iterators import container_bash_files, container_shim_file
from pib_cli.support.iterators.bases import file_copy_base


class DevContainerInstaller(container.DevContainer):
  """Configure a development container with PIB resources."""

  bash_setup_success_message = "Setup Succeeded!"

  def setup(self, notifier: Callable[[str], None]) -> None:
    """Copy pib_cli assets to the container to configure BASH and Python.

    :param notifier: An event handler to notify the user of progress.
    """

    os.makedirs(self.local_executable_folder, exist_ok=True)

    for file in self.get_installation_files():
      shutil.copy(file.source, file.destination)
      notifier(f"Copied: {file.source} -> {file.destination}")

    notifier(self.bash_setup_success_message)

  def get_installation_files(
      self
  ) -> List[file_copy_base.SourceDestinationPair]:
    """Create a list of source / destination file pairs for installation.

    :returns: A list of source / destination file pairs.
    """

    return (
        list(container_bash_files.ContainerBashFilesIterator()) +
        list(container_shim_file.ContainerShimFileIterator())
    )
