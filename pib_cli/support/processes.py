"""Process Management Class"""

import os


class ProcessManager:

  def __init__(self):
    self.exit_code = None

  def spawn_single(self, command):
    result = os.system(command)  # nosec
    self.exit_code = int(result / 256)

  def spawn(self, command_list):
    for command in command_list:
      self.spawn_single(command)
      if self.exit_code != 0:
        return
