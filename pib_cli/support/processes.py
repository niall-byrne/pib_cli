"""Process Management Class."""

import os

from .. import config


class ProcessManager:
  """Manages system calls."""

  def __init__(self):
    self.exit_code = None
    self.overload = None

  def __insert_overload(self):
    """Add the overload parameters as an environment variable."""
    if self.overload:
      overload_string = " ".join(self.overload)
      os.environ[config.ENV_OVERLOAD_ARGUMENTS] = overload_string

  def __clear_overload(self):
    """Clear the overload environment variable."""
    if os.getenv(config.ENV_OVERLOAD_ARGUMENTS, None) is not None:
      os.environ.__delitem__(config.ENV_OVERLOAD_ARGUMENTS)

  def spawn_single(self, command):
    """Execute a single given system call and returns it's exit code.

    :param command: The system call to execute
    :type command: basestring
    :returns: The exit code of the command
    :rtype: int
    """
    result = os.system(command)  # nosec
    self.exit_code = int(result / 256)

  def spawn(self, command_list, overload):
    """Execute a batch of system calls.

    :param command_list: A list of system calls to be executed
    :type command_list: list[basestring]
    :param overload: Extra overloaded arguments specified at the CLI
    :type overload: tuple[basestring]
    """
    self.overload = overload

    self.__insert_overload()
    for command in command_list:
      self.spawn_single(command)
      if self.exit_code != 0:
        break
    self.__clear_overload()
