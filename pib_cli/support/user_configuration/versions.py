"""UserConfigurationVersionBase implementations."""

import os
from typing import Any, Dict, Optional, cast

from pib_cli import config
from pib_cli.config import yaml_keys
from pib_cli.support.user_configuration.bases import (
    version_base,
    version_legacy_base,
)
from pib_cli.support.user_configuration.selectors import (
    command_selector,
    command_selector_legacy,
)


class UserConfigurationV100(
    version_legacy_base.LegacyUserVersionIntermediateBase,
):
  """User configuration for the legacy schema version v1.0.0."""

  version = "1.0.0"
  selector = command_selector_legacy.LegacyCommandSelector


class UserConfigurationV200(
    version_legacy_base.LegacyUserVersionIntermediateBase,
):
  """User configuration for schema version v2.0.0."""

  version = "2.0.0"
  selector = command_selector.CommandSelector


class UserConfigurationV210(version_base.UserConfigurationVersionBase):
  """User configuration for schema version v2.1.0."""

  version = "2.1.0"
  selector = command_selector.CommandSelector

  def get_command_definitions(self) -> Any:
    """Return the CLI command definitions from the configuration."""

    return self.configuration[yaml_keys.V210_CLI_CONFIG_ROOT]

  def get_project_name(self) -> str:
    """Return the project name from the configuration.

    #. Look for an environment variable defined value first.
    #. Look for a configuration file definition next.
    #. Finally, fall back to the default configuration.

    :returns: The configured project name.
    :raises: KeyError
    """

    env_project_name = os.getenv(config.ENV_OVERRIDE_PROJECT_NAME, None)
    metadata = self._get_metadata()
    yaml_project_name = None
    if metadata:
      yaml_project_name = metadata.get(
          yaml_keys.V210_CLI_CONFIG_PROJECT_NAME,
          None,
      )

    if env_project_name:
      return env_project_name
    if metadata and yaml_project_name:
      return yaml_project_name
    raise KeyError(config.ERROR_PROJECT_NAME_NOT_SET)

  def get_documentation_root(self) -> str:
    """Return the documentation folder from the configuration.

    #. Look for an environment variable defined value first.
    #. Look for a configuration file definition next.
    #. Finally, fall back to the default value.

    :returns: The configured documentation folder.
    """
    env_docs_folder = os.getenv(config.ENV_OVERRIDE_DOCUMENTATION_ROOT, None)
    metadata = self._get_metadata()
    yaml_docs_folder = None
    if metadata:
      yaml_docs_folder = metadata.get(
          yaml_keys.V210_CLI_CONFIG_DOCS_FOLDER, None
      )

    if env_docs_folder:
      return env_docs_folder
    if yaml_docs_folder:
      return yaml_docs_folder
    return config.DEFAULT_DOCUMENTATION_FOLDER_NAME

  def _get_metadata(self) -> Optional[Dict[str, str]]:
    return cast(
        Optional[Dict[str, str]],
        self.configuration.get(yaml_keys.V210_CLI_CONFIG_METADATA, None),
    )
