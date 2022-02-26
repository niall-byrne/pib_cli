"""Yaml Configuration Settings."""

from typing import List

from typing_extensions import Final, TypedDict

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
