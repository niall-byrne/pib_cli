"""Generic Configuration Settings."""

ENV_OVERLOAD_ARGUMENTS = 'PIB_OVERLOAD_ARGUMENTS'
ENV_PROJECT_NAME = "PROJECT_NAME"
ENV_OVERRIDE_CONFIG_LOCATION = "PIB_CONFIG_FILE_LOCATION"

ERROR_CONTAINER_ONLY = "This command can only be run inside a PIB container."
ERROR_CONTAINER_VERSION = lambda minimum_version: (
    "This version of pib_cli supports PIB containers version "
    f"{minimum_version} or greater."
)
ERROR_PROJECT_NAME_NOT_SET = (
    f"You must set the {ENV_PROJECT_NAME} variable to use this tool."
)

SETTING_DOCUMENTATION_FOLDER_NAME = "documentation"
