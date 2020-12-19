"""Tests for the CLI Utilities"""

import os
from unittest import TestCase
from unittest.mock import Mock, patch

import patchbay
import yaml
from pib_cli import config_filename
from pib_cli.support.commands import Commands
from .. import yaml_keys


class MockPathManager:

  def __init__(self):
    self.project_root = Mock()
    self.project_docs = Mock()
    self.is_container = Mock()
    self.is_container.return_value = True


class MockProcessManager:

  def __init__(self):
    self.exit_code = None
    self.spawn_single = Mock()
    self.spawn = Mock()


class CommandTestHarness(TestCase):
  __test__ = False
  command = None
  overload = None

  def get_yaml_entry(self, name):
    for entry in self.yaml:
      if entry[yaml_keys.COMMAND_NAME] == name:
        self.config = entry
        return
    raise KeyError("Could not find yaml key name: %s" % name)

  @classmethod
  def setUpClass(cls):
    with open(config_filename) as file_handle:
      cls.yaml = yaml.safe_load(file_handle)

  @patch(patchbay.COMMANDS_PATH_MANAGER)
  @patch(patchbay.COMMANDS_PROCESS_MANAGER)
  def setUp(self, mock_proc, mock_path):  # pylint: disable=arguments-differ
    self.command = self.__class__.command
    self.overload = self.__class__.overload
    self.path_manager = MockPathManager()
    self.proc_manager = MockProcessManager()

    mock_path.return_value = self.path_manager
    mock_proc.return_value = self.proc_manager

    self.cmd_mgr = Commands()
    self.get_yaml_entry(self.command)

  def test_invoke_uses_correct_path(self):
    self.cmd_mgr.invoke(self.command)
    method = getattr(self.path_manager, self.config[yaml_keys.PATH_METHOD])
    method.assert_called_once_with()

  def test_successful_system_calls(self):
    self.proc_manager.exit_code = 0
    self.cmd_mgr.invoke(self.command, overload=self.overload)

    expected_commands = self.cmd_mgr.coerce_from_string_to_list(
        self.config[yaml_keys.COMMANDS])
    self.proc_manager.spawn.assert_called_once_with(expected_commands)

  @patch(patchbay.COMMANDS_OS_ENVIRON)
  def test_successful_overload(self, mock_environ):
    mock_setter = Mock()
    mock_environ.return_value = os.environ
    mock_environ.__getitem__.side_effect = os.environ.__getitem__
    mock_environ.__setitem__ = mock_setter

    if self.overload:

      overload_string = " ".join(self.overload)
      self.proc_manager.exit_code = 0
      self.cmd_mgr.invoke(self.command, overload=self.overload)
      mock_setter.called_once_with(
          self.cmd_mgr.overload_env_name,
          overload_string,
      )

  def test_successful_results(self):
    self.proc_manager.exit_code = 0
    result = self.cmd_mgr.invoke(self.command)
    self.assertEqual(self.cmd_mgr.process_manager.exit_code,
                     self.proc_manager.exit_code)
    self.assertEqual(result, self.config[yaml_keys.SUCCESS])

  def test_unsuccessful_system_calls(self):
    self.proc_manager.exit_code = 1
    self.cmd_mgr.invoke(self.command)
    expected_commands = self.cmd_mgr.coerce_from_string_to_list(
        self.config[yaml_keys.COMMANDS])
    self.proc_manager.spawn.assert_called_once_with(expected_commands)

  def test_unsuccessful_results(self):
    self.proc_manager.exit_code = 1
    result = self.cmd_mgr.invoke(self.command)
    self.assertEqual(self.cmd_mgr.process_manager.exit_code,
                     self.proc_manager.exit_code)
    self.assertEqual(result, self.config[yaml_keys.FAILURE])
