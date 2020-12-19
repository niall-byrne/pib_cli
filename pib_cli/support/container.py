"""CLI Container Management"""

import os

from .. import config


class ContainerManager:

  @staticmethod
  def is_container():
    return os.path.exists(config.SETTING_CONTAINER_MARKER)
