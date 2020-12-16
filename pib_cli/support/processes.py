"""CLI Process Management"""
import os


class ProcessManager:

  def __init__(self):
    self.exit_code = None

  def spawn(self, command):
    result = os.system(command)  # nosec
    self.exit_code = int(result / 256)
