"""Initial Environment Setup and Discovery"""

import os
import pathlib

from . import config

project_root = pathlib.Path(__file__).parent.absolute()


def get_config_file_name():
  """Get the full path of the yaml configuration file to be used

  :returns: The path to the configuration file
  :rtype: basestring
  """
  override = os.getenv(config.ENV_OVERRIDE_CONFIG_LOCATION, None)
  if override:
    return override
  return os.path.join(project_root, "config/config.yml")


def check_project_name():
  if config.ENV_PROJECT_NAME not in os.environ:
    raise KeyError(config.ERROR_PROJECT_NAME_NOT_SET)


check_project_name()
config_filename = get_config_file_name()
