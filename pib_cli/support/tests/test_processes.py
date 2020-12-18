"""Test the Process Manager"""

from unittest import TestCase
from unittest.mock import patch

from pib_cli.support.processes import ProcessManager


class TestProcessManager(TestCase):

  def setUp(self):
    self.process_manager = ProcessManager()

  def test_initial_instance_variables(self):
    self.assertIsNone(self.process_manager.exit_code)

  def test_spawn_single_clean_exit_code(self):
    self.process_manager.spawn_single("exit 0")
    self.assertEqual(
        self.process_manager.exit_code,
        0,
    )

  def test_spawn_single_unclean_exit_code(self):
    self.process_manager.spawn_single("exit 1")
    self.assertEqual(
        self.process_manager.exit_code,
        1,
    )

  @patch("pib_cli.support.processes.ProcessManager.spawn_single")
  def test_batch_spawn_correct_command_called_success(self, mock_spawn):
    command = ["echo 1", "echo 2"]

    self.process_manager.exit_code = 0
    self.process_manager.spawn(command)

    mock_spawn.assert_any_call(command[0])
    mock_spawn.assert_any_call(command[1])
    self.assertEqual(self.process_manager.exit_code, 0)
    self.assertEqual(mock_spawn.call_count, len(command))

  @patch("pib_cli.support.processes.ProcessManager.spawn_single")
  def test_batch_spawn_correct_command_called_failure(self, mock_spawn):
    command = ["exit 1", "exit 2"]

    self.process_manager.exit_code = 1
    self.process_manager.spawn(command)

    mock_spawn.assert_any_call(command[0])
    self.assertEqual(self.process_manager.exit_code, 1)
    self.assertEqual(mock_spawn.call_count, 1)

  @patch("pib_cli.support.processes.os.system")
  def test_spawn_single_correct_command_called_success(self, mock_system_call):
    mock_system_call.return_value = 0
    command = "exit 0"

    self.process_manager.spawn_single(command)

    mock_system_call.assert_called_once_with(command)
    self.assertEqual(self.process_manager.exit_code, 0)

  @patch("pib_cli.support.processes.os.system")
  def test_spawn_single_correct_command_called_failure(self, mock_system_call):
    mock_system_call.return_value = 256
    command = "exit 1"

    self.process_manager.spawn_single(command)

    mock_system_call.assert_called_once_with(command)
    self.assertEqual(self.process_manager.exit_code, 1)
