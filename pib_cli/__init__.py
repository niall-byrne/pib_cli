"""Initial Environment Setup and Discovery."""

import os
import pathlib

import click

from . import config
from .config.locale import _

project_root = pathlib.Path(__file__).parent.absolute()
default_config = os.path.join(project_root, "config/config.yml")


def get_config_file_name() -> str:
  """Get the full path of the yaml configuration file to be used.

  :returns: The path to the configuration file
  """
  override = os.getenv(config.ENV_OVERRIDE_CONFIG_LOCATION, None)
  if override and os.path.exists(override):
    return override
  click.echo(_("** PIB DEFAULT CONFIG IN USE **"))
  return default_config


def check_project_name() -> None:
  """Get the current project name from the environment.

  :raises: KeyError
  """

  if config.ENV_PROJECT_NAME not in os.environ:
    raise KeyError(config.ERROR_PROJECT_NAME_NOT_SET)


check_project_name()
config_filename = get_config_file_name()
