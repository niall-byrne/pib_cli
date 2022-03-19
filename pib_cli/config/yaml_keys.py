"""YAML configuration settings."""

from typing import List

from typing_extensions import Final, TypedDict

V210_CLI_CONFIG_ROOT: Final = 'cli_definition'
V210_CLI_CONFIG_PROJECT_NAME: Final = 'project_name'

CONTAINER_ONLY: Final = 'container_only'
PATH_METHOD: Final = 'path'
COMMANDS: Final = 'commands'
SUCCESS: Final = 'success'
FAILURE: Final = 'failure'
COMMAND_NAME: Final = 'name'
COMMAND_DESCRIPTION: Final = 'description'

TypeUserConfiguration = TypedDict(
    'TypeUserConfiguration', {
        'name': str,
        'description': str,
        'container_only': bool,
        'path': str,
        'commands': List[str],
        'success': str,
        'failure': str,
    },
    total=False
)
