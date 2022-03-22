"""UserConfigurationFile class."""

import os
import pathlib
from typing import List, Optional, Type

import pib_cli
from pib_cli import config
from pib_cli.config.locale import _
from pib_cli.support import path_map
from pib_cli.support.mixins import text_file, yaml_file

from . import validator, versions
from .bases import version_base

TypeVersion = Type[version_base.UserConfigurationVersionBase]


class UserConfigurationFile(yaml_file.YAMLFileReader, text_file.TextFileReader):
  """The end-user's pib_cli configuration file."""

  supported_versions: List[TypeVersion] = [
      versions.UserConfigurationV210,
      versions.UserConfigurationV200,
      versions.UserConfigurationV100,
  ]

  def __init__(self, config_file: Optional[str] = None) -> None:
    self.git_root_folder = path_map.PathMap().git_root_folder
    self.project_root = pathlib.Path(pib_cli.__file__).parent.absolute()
    self.specified_file_name = config_file
    self.default_config = os.path.join(
        self.project_root, "config", "default_cli_config.yml"
    )

  def get_config_file_name(self) -> str:
    """Get the full path of the yaml configuration file.

    #. Look for a manually specified file first,
    #. Look for an environment variable defined file next.
    #. Look for a configuration file in the repository root folder next.
    #. Finally, fall back to the default configuration.

    :returns: The path to the configuration file.
    """

    if self.specified_file_name:
      return str(pathlib.Path(self.specified_file_name).resolve())

    for option in [
        os.getenv(config.ENV_OVERRIDE_CONFIG_LOCATION, None),
        os.path.join(self.git_root_folder, config.PIB_CONFIG_FILE_NAME),
    ]:
      if option and os.path.exists(option):
        break
    else:
      return self.default_config

    return option

  def get_raw_file(self) -> str:
    """Return the configuration file from disk.

    :returns: The configuration file from disk.
    """

    return self.load_text_file(self.get_config_file_name()).rstrip()

  def parse(self) -> version_base.UserConfigurationVersionBase:
    """Load, validate and detect the version of the UserConfiguration.

    :returns: A class representing the detected version of config.
    :raises: :class:`NotImplementedError`
    """

    configuration_yaml = self.load_yaml_file(self.get_config_file_name())
    configuration_validator = validator.UserConfigurationValidator()
    detected_version = configuration_validator.validate(configuration_yaml)

    for user_configuration in self.supported_versions:
      if detected_version == user_configuration.version:
        return user_configuration(configuration_yaml)

    raise NotImplementedError(
        _("Configuration version {detected_version} is not supported!").format(
            detected_version=detected_version
        )
    )
