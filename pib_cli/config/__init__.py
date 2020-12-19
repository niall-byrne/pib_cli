"""Generic Configuration Settings"""

import os

CONTAINER_ONLY_ERROR = "This command can only be run inside a PIB container."
CONTAINER_MARKER = os.path.join("/", "etc", "container_release")
