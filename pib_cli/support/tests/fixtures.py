"""Tests for the CLI Utilities"""

from unittest import TestCase
from unittest.mock import Mock, patch

import yaml
from pib_cli import config_filename
from pib_cli.support.commands import Commands


class MockPathManager:

  def __init__(self):
    self.project_root = Mock()
    self.project_docs = Mock()


class MockProcessManager:

  def __init__(self):
    self.exit_code = None
    self.spawn_single = Mock()
    self.spawn = Mock()


class CommandTestHarness(TestCase):
  __test__ = False
  command = None

  def get_yaml_entry(self, name):
    for entry in self.yaml:
      if entry['name'] == name:
        self.config = entry
        return
    raise KeyError("Could not find yaml key name: %s" % name)

  @classmethod
  def setUpClass(cls):
    with open(config_filename) as file_handle:
      cls.yaml = yaml.load(file_handle, Loader=yaml.SafeLoader)

  @patch("pib_cli.support.commands.PathManager")
  @patch("pib_cli.support.commands.ProcessManager")
  def setUp(self, mock_proc, mock_path):  # pylint: disable=arguments-differ
    self.command = self.__class__.command
    self.path_manager = MockPathManager()
    self.proc_manager = MockProcessManager()

    mock_path.return_value = self.path_manager
    mock_proc.return_value = self.proc_manager

    self.commands = Commands()
    self.get_yaml_entry(self.command)

  def test_invoke_uses_correct_path(self):
    self.commands.invoke(self.command)
    method = getattr(self.path_manager, self.config['path_method'])
    method.assert_called_once_with()

  def test_successful_system_calls(self):
    self.proc_manager.exit_code = 0
    self.commands.invoke(self.command)
    self.proc_manager.spawn.assert_called_once_with(self.config['commands'])

  def test_successful_results(self):
    self.proc_manager.exit_code = 0
    result = self.commands.invoke(self.command)
    self.assertEqual(self.commands.process_manager.exit_code,
                     self.proc_manager.exit_code)
    self.assertEqual(result, self.config['success'])

  def test_unsuccessful_system_calls(self):
    self.proc_manager.exit_code = 1
    self.commands.invoke(self.command)
    self.proc_manager.spawn.assert_called_once_with(self.config['commands'])

  def test_unsuccessful_results(self):
    self.proc_manager.exit_code = 1
    result = self.commands.invoke(self.command)
    self.assertEqual(self.commands.process_manager.exit_code,
                     self.proc_manager.exit_code)
    self.assertEqual(result, self.config['failure'])