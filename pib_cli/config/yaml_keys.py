"""Yaml Configuration Settings."""

from typing import List

from typing_extensions import Final, TypedDict

CONTAINER_ONLY: Final = 'container_only'
PATH_METHOD: Final = 'path'
COMMANDS: Final = 'commands'
SUCCESS: Final = 'success'
FAILURE: Final = 'failure'
COMMAND_NAME: Final = 'name'

TypeUserConfiguration = TypedDict(
    'TypeUserConfiguration', {
        'container_only': bool,
        'path': str,
        'commands': List[str],
        'success': str,
        'failure': str,
        'name': str,
    },
    total=False
)
