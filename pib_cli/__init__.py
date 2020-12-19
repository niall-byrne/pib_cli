"""Find and Load Configuration"""

import os
import pathlib

from . import config

project_root = pathlib.Path(__file__).parent.absolute()


def get_config_file_name():
  override = os.getenv(config.ENV_OVERRIDE_CONFIG_LOCATION, None)
  if override:
    return override
  return os.path.join(project_root, "config/config.yml")


config_filename = get_config_file_name()
