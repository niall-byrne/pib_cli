"""UserConfigurationVersionBase implementations."""

import os
from typing import Any, cast

from pib_cli import config
from pib_cli.config import yaml_keys

from .bases import user_configuration_base


class UserConfigurationV200(
    user_configuration_base.UserConfigurationVersionBase
):
  """User configuration for schema version v2.0.0."""

  version = "2.0.0"

  def get_command_definitions(self) -> Any:
    """Return the CLI command definitions from the configuration."""

    return self.configuration

  def get_project_name(self) -> str:
    """Return the project name from the configuration.

    :returns: The configured project name
    :raises: KeyError
    """

    project_name = os.getenv(config.ENV_PROJECT_NAME, None)

    if project_name:
      return project_name
    raise KeyError(config.ERROR_PROJECT_NAME_NOT_SET)


class UserConfigurationV210(
    user_configuration_base.UserConfigurationVersionBase
):
  """User configuration for schema version v2.1.0."""

  version = "2.1.0"

  def get_command_definitions(self) -> Any:
    """Return the CLI command definitions from the configuration."""

    return self.configuration[yaml_keys.V210_CLI_CONFIG_ROOT]

  def get_project_name(self) -> str:
    """Return the project name from the configuration.

    #. Look for an environment variable defined value first.
    #. Look for a configuration file definition next.
    #. Finally, fall back to the default configuration.

    :returns: The configured project name
    :raises: KeyError
    """

    env_project_name = os.getenv(config.ENV_PROJECT_NAME, None)
    yaml_project_name = self.configuration.get(
        yaml_keys.V210_CLI_CONFIG_PROJECT_NAME,
        None,
    )

    if env_project_name:
      return env_project_name
    if yaml_project_name:
      return cast(str, yaml_project_name)
    raise KeyError(config.ERROR_PROJECT_NAME_NOT_SET)
