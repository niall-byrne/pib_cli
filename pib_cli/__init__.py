"""Find and Load Configuration"""

import os
import pathlib

project_root = pathlib.Path(__file__).parent.absolute()
config_filename = os.path.join(project_root, "config.yml")
