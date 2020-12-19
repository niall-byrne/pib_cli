"""Test the Process Manager"""

import os
from unittest import TestCase
from unittest.mock import Mock, patch

from ... import config, patchbay
from ..processes import ProcessManager


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

  @patch(patchbay.PROCESS_MANAGER_SPAWN_SINGLE)
  @patch(patchbay.PROCESS_MANAGER_OS_ENVIRON)
  def test_batch_spawn_overload_is_set(
      self,
      mock_environ,
      _,
  ):
    mock_environ_dict = dict(os.environ)
    mock_setter = Mock()
    mock_environ.return_value = mock_environ_dict

    mock_environ.__setitem__ = mock_setter

    command = ["echo 1", "echo 2"]
    overload = ["some", "overload", "list"]

    self.process_manager.exit_code = 0
    self.process_manager.spawn(command, overload)

    mock_setter.assert_called_once_with(
        config.ENV_OVERLOAD_ARGUMENTS,
        " ".join(overload),
    )

  @patch(patchbay.PROCESS_MANAGER_SPAWN_SINGLE)
  @patch(patchbay.PROCESS_MANAGER_OS_ENVIRON)
  def test_batch_spawn_overload_is_deleted(
      self,
      mock_environ,
      _,
  ):
    mock_environ_dict = dict(os.environ)
    mock_deleter = Mock()
    mock_environ.return_value = mock_environ_dict

    mock_environ.__delitem__ = mock_deleter
    mock_environ.__getitem__.return_value = "Some Value"

    command = ["echo 1", "echo 2"]
    overload = ["some", "overload", "list"]

    self.process_manager.exit_code = 0
    self.process_manager.spawn(command, overload)

    mock_deleter.assert_called_once_with(config.ENV_OVERLOAD_ARGUMENTS)

  @patch(patchbay.PROCESS_MANAGER_SPAWN_SINGLE)
  @patch(patchbay.PROCESS_MANAGER_OS_ENVIRON)
  def test_batch_spawn_overload_is_deleted_on_fail(
      self,
      mock_environ,
      _,
  ):
    mock_environ_dict = dict(os.environ)
    mock_deleter = Mock()
    mock_environ.return_value = mock_environ_dict

    mock_environ.__delitem__ = mock_deleter
    mock_environ.__getitem__.return_value = "Some Value"

    command = ["echo 1", "echo 2"]
    overload = ["some", "overload", "list"]

    self.process_manager.exit_code = 99
    self.process_manager.spawn(command, overload)

    mock_deleter.assert_called_once_with(config.ENV_OVERLOAD_ARGUMENTS)

  @patch(patchbay.PROCESS_MANAGER_SPAWN_SINGLE)
  def test_batch_spawn_correct_command_called_success(self, mock_spawn):
    command = ["exit 1", "exit 2"]

    self.process_manager.exit_code = 0
    self.process_manager.spawn(command, None)

    mock_spawn.assert_any_call(command[0])
    mock_spawn.assert_any_call(command[1])
    self.assertEqual(self.process_manager.exit_code, 0)
    self.assertEqual(mock_spawn.call_count, len(command))
    self.assertEqual(self.process_manager.overload, None)

  @patch(patchbay.PROCESS_MANAGER_SPAWN_SINGLE)
  def test_batch_spawn_correct_command_called_failure(self, mock_spawn):
    command = ["exit 1", "exit 2"]

    self.process_manager.exit_code = 1
    self.process_manager.spawn(command, None)

    mock_spawn.assert_any_call(command[0])
    self.assertEqual(self.process_manager.exit_code, 1)
    self.assertEqual(mock_spawn.call_count, 1)
    self.assertEqual(self.process_manager.overload, None)

  @patch(patchbay.PROCESS_MANAGER_OS_SYSTEM)
  def test_spawn_single_correct_command_called_success(self, mock_system_call):
    mock_system_call.return_value = 0
    command = "exit 0"

    self.process_manager.spawn_single(command)

    mock_system_call.assert_called_once_with(command)
    self.assertEqual(self.process_manager.exit_code, 0)

  @patch(patchbay.PROCESS_MANAGER_OS_SYSTEM)
  def test_spawn_single_correct_command_called_failure(self, mock_system_call):
    mock_system_call.return_value = 256
    command = "exit 1"

    self.process_manager.spawn_single(command)

    mock_system_call.assert_called_once_with(command)
    self.assertEqual(self.process_manager.exit_code, 1)
