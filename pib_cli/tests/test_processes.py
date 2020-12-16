"""Test the Process Manager"""

from unittest import TestCase
from unittest.mock import patch

from pib_cli.support.processes import ProcessManager


class TestProcessManager(TestCase):

  def setUp(self):
    self.process_manager = ProcessManager()

  def test_initial_instance_variables(self):
    assert self.process_manager.exit_code is None

  def test_simple_spawn_clean_exit_code(self):
    self.process_manager.spawn("exit 0")
    assert self.process_manager.exit_code == 0

  def test_simple_spawn_unclean_exit_code(self):
    self.process_manager.spawn("exit 1")
    assert self.process_manager.exit_code == 1

  @patch("pib_cli.support.processes.os.system")
  def test_simple_spawn_correct_command_called(self, mock_system_call):
    mock_system_call.return_value = 256
    command = "exit 1"

    self.process_manager.spawn(command)

    mock_system_call.assert_called_once_with(command)
    assert self.process_manager.exit_code == 1
