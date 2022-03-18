"""DevContainer class."""

import os

from packaging import version
from pib_cli import config

from . import exceptions
from .bases import container


class DevContainer(container.DevContainerBase):
  """Containerized development environment."""

  def container_valid_exception(self) -> None:
    """Raise the appropriate exception if the environment is invalid.

    :raises: :class:`DevContainerException`
    """
    if not self.is_container():
      self.container_only_exception()
    if not self.is_compatible_container():
      self.container_version_exception()

  def container_only_exception(self) -> None:
    """Raise an exception for commands that must be run inside a container.

    :raises: :class:`DevContainerException`
    """
    raise exceptions.DevContainerException(
        config.ERROR_CONTAINER_ONLY, exit_code=config.EXIT_CODE_CONTAINER_ONLY
    )

  def container_version_exception(self) -> None:
    """Raise an exception for a container with the wrong version information.

    :raises: :class:`DevContainerException`
    """
    raise exceptions.DevContainerException(
        config.ERROR_CONTAINER_VERSION(self.minimum_pib_version,),
        exit_code=config.EXIT_CODE_CONTAINER_INCOMPATIBLE,
    )

  def is_container(self) -> bool:
    """Determine if the current environment is a development container.

    :returns: A boolean indicating if the command is executing in a container.
    """
    return os.path.exists(self.file_container_marker)

  def is_compatible_container(self) -> bool:
    """Determine if the current environment is a compatible container.

    :returns: A boolean indicating if the container is a matching version.
    """
    return (
        version.parse(self.get_container_version()) >=
        version.parse(self.minimum_pib_version)
    )

  def get_container_version(self) -> str:
    """Return the the PIB container's version, or raise an exception.

    :returns: The current version of the container.
    :raises: :class:`DevContainerException`
    """
    if not self.is_container():
      self.container_only_exception()

    try:
      return self.load_text_file(self.file_version_marker).strip()
    except FileNotFoundError:
      return self.unversioned_pib_value
