"""Generic Configuration Settings."""

import os

ENV_OVERLOAD_ARGUMENTS = 'PIB_OVERLOAD_ARGUMENTS'
ENV_PROJECT_NAME = "PROJECT_NAME"
ENV_OVERRIDE_CONFIG_LOCATION = "PIB_CONFIG_FILE_LOCATION"

ERROR_CONTAINER_ONLY = "This command can only be run inside a PIB container."
ERROR_PROJECT_NAME_NOT_SET = (
    f"You must set the {ENV_PROJECT_NAME} variable to use this tool."
)

SETTING_BASH_SETUP_SUCCESS_MESSAGE = "Setup Succeeded!"
SETTING_CONTAINER_MARKER = os.path.join("/", "etc", "container_release")
SETTING_DOCUMENTATION_FOLDER_NAME = "documentation"
SETTING_PROJECT_ROOT_NAME = "app"

LOCAL_EXECUTABLES = "/home/user/.local/bin"
