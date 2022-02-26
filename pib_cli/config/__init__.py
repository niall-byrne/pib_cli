"""Generic Configuration Settings."""

from typing import Callable, Union

from pib_cli.config.locale import _

PIB_URL = "https://github.com/niall-byrne/python-in-a-box"
DOCUMENTATION_FOLDER_NAME = "documentation"

ENV_OVERLOAD_ARGUMENTS = 'PIB_OVERLOAD_ARGUMENTS'
ENV_PROJECT_NAME = "PROJECT_NAME"
ENV_OVERRIDE_CONFIG_LOCATION = "PIB_CONFIG_FILE_LOCATION"

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
    f"You must set the {ENV_PROJECT_NAME} variable to use this tool."
)
