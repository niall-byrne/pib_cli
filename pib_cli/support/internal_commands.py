"""CLI External Command Management Class"""

import glob
import os
import shutil
from pathlib import Path

import click

from .. import config, project_root
from .container import ContainerManager


def setup_bash():
  """Configures the BASH environment for a development container.

  :returns: A success message, if the command completes sucessfully.
  :rtype: basestring
  """

  if not ContainerManager.is_container():
    return config.ERROR_CONTAINER_ONLY

  results = []
  bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
  home_dir = str(Path.home())
  for file_name in bash_files:
    shutil.copy(file_name, home_dir)
    results.append(f"Copied: {file_name} -> {home_dir} ")
  results.append(config.SETTING_BASH_SETUP_SUCCESS_MESSAGE)
  return "\n".join(results)


def execute_internal_command(commands):
  """Executes a batch of internal python commands.

  :param commands: A list of commands to be executed
  :type commands: list[basestring]
  """

  for command in commands:
    response = globals()[command]()
    click.echo(response)
