"""Process Management Class"""

import os

from .. import config


class ProcessManager:

  def __init__(self):
    self.exit_code = None
    self.overload = None

  def __insert_overload(self):
    if self.overload:
      overload_string = " ".join(self.overload)
      os.environ[config.ENV_OVERLOAD_ARGUMENTS] = overload_string

  def __clear_overload(self):
    if os.getenv(config.ENV_OVERLOAD_ARGUMENTS, None) is not None:
      os.environ.__delitem__(config.ENV_OVERLOAD_ARGUMENTS)

  def spawn_single(self, command):
    result = os.system(command)  # nosec
    self.exit_code = int(result / 256)

  def spawn(self, command_list, overload):
    self.overload = overload

    self.__insert_overload()
    for command in command_list:
      self.spawn_single(command)
      if self.exit_code != 0:
        break
    self.__clear_overload()
