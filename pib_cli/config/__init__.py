"""Python-in-a-Box CLI configuration settings."""

from typing import Callable

from pib_cli.config import yaml_keys
from pib_cli.config.locale import _

PIB_URL = "https://github.com/niall-byrne/python-in-a-box"
PIB_CONFIG_FILE_NAME = ".pib.yml"

DEFAULT_DOCUMENTATION_FOLDER_NAME = "documentation"

ENV_OVERLOAD_ARGUMENTS = 'PIB_OVERLOAD_ARGUMENTS'
ENV_OVERRIDE_CONFIG_LOCATION = "PIB_CONFIG_FILE_LOCATION"
ENV_OVERRIDE_DOCUMENTATION_ROOT = "PIB_DOCUMENTATION_ROOT"
ENV_OVERRIDE_PROJECT_NAME = "PIB_PROJECT_NAME"


ERROR_CONTAINER_ONLY = _(
    "This command can only be run inside a PIB container.\n"
    "Find out more here: {PIB_URL}"
).format(PIB_URL=PIB_URL)

ERROR_CONTAINER_VERSION: Callable[[str], str] = \
    lambda minimum_version: _(
        "This command can only be run inside a PIB container with version "
        "{minimum_version} or greater.\n"
        "Find out more here: {PIB_URL}"
    ).format(minimum_version=minimum_version, PIB_URL=PIB_URL)
ERROR_PROJECT_NAME_NOT_SET = (
    f"You must set the {ENV_OVERRIDE_PROJECT_NAME} variable, or the "
    f"'{yaml_keys.V210_CLI_CONFIG_PROJECT_NAME}' config key "
    "to use this tool."
)

EXIT_CODE_CONTAINER_ONLY = 127
EXIT_CODE_CONTAINER_INCOMPATIBLE = 126
EXIT_CODE_NOT_A_REPOSITORY = 125
EXIT_CODE_DOCUMENTATION_ROOT_NOT_FOUND = 124
EXIT_CODE_PROJECT_NAME_ROOT_NOT_FOUND = 123
