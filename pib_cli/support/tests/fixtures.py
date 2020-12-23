"""Tests for the CLI Utilities"""

from unittest import TestCase
from unittest.mock import Mock, patch

import yaml

from ... import config_filename, patchbay
from ...config import yaml_keys
from ..external_commands import ExternalCommands


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

  def get_coerced_from_string_commands(self):
    if isinstance(self.config[yaml_keys.COMMANDS], str):
      return [self.config[yaml_keys.COMMANDS]]
    return self.config[yaml_keys.COMMANDS]

  @classmethod
  def setUpClass(cls):
    with open(config_filename) as file_handle:
      cls.yaml = yaml.safe_load(file_handle)

  @patch(patchbay.PATH_MANAGER_CONTAINER_PATH_MANAGER)
  @patch(patchbay.EXTERNAL_COMMANDS_PROCESS_MANAGER)
  def setUp(self, mock_proc, mock_path):  # pylint: disable=arguments-differ
    self.command = self.__class__.command
    self.overload = self.__class__.overload
    self.path_manager = MockPathManager()
    self.proc_manager = MockProcessManager()

    mock_path.return_value = self.path_manager
    mock_proc.return_value = self.proc_manager

    with patch(patchbay.CONTAINER_MANAGER_IS_CONTAINER, return_value=True):
      self.cmd_mgr = ExternalCommands()

    self.get_yaml_entry(self.command)

  def test_invoke_uses_correct_path(self):
    self.cmd_mgr.invoke(self.command, self.overload)
    method = getattr(self.path_manager, self.config[yaml_keys.PATH_METHOD])
    method.assert_called_once_with()

  def test_successful_system_calls(self):
    self.proc_manager.exit_code = 0
    self.cmd_mgr.invoke(self.command, self.overload)

    expected_commands = self.get_coerced_from_string_commands()
    self.proc_manager.spawn.assert_called_once_with(
        expected_commands, self.overload
    )

  def test_successful_results(self):
    self.proc_manager.exit_code = 0
    result = self.cmd_mgr.invoke(self.command, self.overload)
    self.assertEqual(
        self.cmd_mgr.process_manager.exit_code, self.proc_manager.exit_code
    )
    self.assertEqual(result, self.config[yaml_keys.SUCCESS])

  def test_unsuccessful_system_calls(self):
    self.proc_manager.exit_code = 1
    self.cmd_mgr.invoke(self.command, self.overload)
    expected_commands = self.get_coerced_from_string_commands()
    self.proc_manager.spawn.assert_called_once_with(
        expected_commands, self.overload
    )

  def test_unsuccessful_results(self):
    self.proc_manager.exit_code = 1
    result = self.cmd_mgr.invoke(self.command, self.overload)
    self.assertEqual(
        self.cmd_mgr.process_manager.exit_code, self.proc_manager.exit_code
    )
    self.assertEqual(result, self.config[yaml_keys.FAILURE])
