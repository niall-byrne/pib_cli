"""CLI Internal Command Management Class"""

import glob
import os
import shutil
from pathlib import Path

import click
import pkg_resources

from .. import config, get_config_file_name, project_root
from .container import ContainerManager
from .paths import get_path_manager
from .processes import ProcessManager


class InternalCommands:
  """Methods for implementing internal Python-based commands."""

  def __init__(self):
    self.process_manager = ProcessManager()
    self.path_manager = get_path_manager()

  def config_location(self):
    """Report the location of the current active config.

    :returns: A success message, if the command completes successfully.
    :rtype: basestring
    """
    current_config = get_config_file_name()
    return f"Current Configuration: {current_config}"

  def config_show(self):
    """Exports the current active configuration.

    :returns: A success message, if the command completes successfully.
    :rtype: basestring
    """
    current_config = get_config_file_name()
    with open(current_config) as fhandle:
      results = fhandle.read().strip()
    return results

  def setup_bash(self):
    """Configures the BASH environment for a development container.

    :returns: A success message, if the command completes successfully.
    :rtype: basestring
    """

    if not ContainerManager.is_container():
      return config.ERROR_CONTAINER_ONLY

    results = []
    bash_files = glob.glob(os.path.join(project_root, "bash", "*"))
    home_dir = str(Path.home())
    for file_name in bash_files:
      dotted_name = "." + os.path.basename(file_name)
      destination = os.path.join(home_dir, dotted_name)
      shutil.copy(file_name, destination)
      results.append(f"Copied: {file_name} -> {destination} ")
    results.append(config.SETTING_BASH_SETUP_SUCCESS_MESSAGE)
    return "\n".join(results)

  def version(self):
    return (
        "pib_cli version: "
        f"{pkg_resources.get_distribution('pib_cli').version}"
    )


def execute_internal_command(commands):
  """Executes a batch of internal python commands.

  :param commands: A list of commands to be executed
  :type commands: list[basestring]
  """

  internal_commands = InternalCommands()

  for command in commands:
    response = getattr(internal_commands, command)()
    click.echo(response)
