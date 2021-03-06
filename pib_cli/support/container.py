"""Container Management Class"""

import os

from .. import config


class ContainerManager:
  """Methods relating to the presence of a development environment container."""

  @staticmethod
  def is_container():
    """Determines if the current environment is a development container.

    :returns: A boolean indicating if the command is executing in a container
    :rtype: bool
    """
    return os.path.exists(config.SETTING_CONTAINER_MARKER)
