"""LegacyUserVersionIntermediateBase class."""

import os
from typing import Any, Type

from pib_cli import config

from . import command_selector_base
from .version_base import UserConfigurationVersionBase


class LegacyUserVersionIntermediateBase(UserConfigurationVersionBase):
  """An intermediate base class for older json schemas."""

  version: str
  selector: Type[command_selector_base.CommandSelectorBase]

  def get_project_name(self) -> str:
    """Return the project name from the configuration.

    :returns: The configured project name
    :raises: KeyError
    """

    project_name = os.getenv(config.ENV_OVERRIDE_PROJECT_NAME, None)

    if project_name:
      return project_name
    raise KeyError(config.ERROR_PROJECT_NAME_NOT_SET)

  def get_command_definitions(self) -> Any:
    """Return the CLI command definitions from the configuration."""

    return self.configuration
