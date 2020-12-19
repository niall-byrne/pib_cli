"""Find and Load Configuration"""

import os
import pathlib

CONFIG_LOCATION_ENV_OVERRIDE = "PIB_CONFIG_FILE_LOCATION"

project_root = pathlib.Path(__file__).parent.absolute()


def get_config_file_name():
  override = os.getenv(CONFIG_LOCATION_ENV_OVERRIDE, None)
  if override:
    return override
  return os.path.join(project_root, "config/config.yml")


config_filename = get_config_file_name()
