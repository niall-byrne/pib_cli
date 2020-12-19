"""CLI Container Management"""

import os

import config


class ContainerManager:

  @staticmethod
  def is_container():
    return os.path.exists(config.CONTAINER_MARKER)
