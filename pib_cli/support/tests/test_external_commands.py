"""Tests for External Command Invocations"""

from unittest import TestCase
from unittest.mock import patch

from config import yaml_keys

from ... import config, patchbay
from ..configuration import ConfigurationManager
from ..external_commands import ExternalCommands
from ..paths import PathManager
from ..processes import ProcessManager
from .fixtures import CommandTestHarness


class TestCommandClass(TestCase):

  def yaml_test_data(self, path_method, test_command, container_only):
    return {
        yaml_keys.COMMAND_NAME: test_command,
        yaml_keys.CONTAINER_ONLY: container_only,
        yaml_keys.PATH_METHOD: path_method,
        yaml_keys.COMMANDS: "Some Command"
    }

  def setUp(self):
    self.commands = ExternalCommands()

  def test_initial_instance_variables(self):
    self.assertIsInstance(self.commands.process_manager, ProcessManager)
    self.assertIsInstance(self.commands.path_manager, PathManager)
    self.assertIsInstance(
        self.commands.configuration_manager, ConfigurationManager
    )

  def test_invoke_non_existent_command(self):
    with self.assertRaises(KeyError):
      self.commands.invoke("non-existent-command")

  def test_invoke_non_existent_command_with_options(self):
    with self.assertRaises(KeyError):
      self.commands.invoke("non-existent-command", overload=('option1',))

  @patch(patchbay.CONFIGURATION_MANAGER_IS_CONFIG_EXECUTABLE)
  @patch(patchbay.CONFIGURATION_MANAGER_FIND_CONFIG)
  def test_outside_container_flag_fails(self, mock_config, mock_exec):
    mock_config.return_value = None
    mock_exec.return_value = False

    response = self.commands.invoke("test_command")
    self.assertEqual(response, config.ERROR_CONTAINER_ONLY)
    self.assertEqual(0, self.commands.process_manager.exit_code)

  @patch(patchbay.CONFIGURATION_MANAGER_IS_CONFIG_EXECUTABLE)
  @patch(patchbay.CONFIGURATION_MANAGER_FIND_CONFIG)
  @patch(patchbay.CONFIGURATION_MANAGER_GET_CONFIG_PATH_METHOD)
  def test_outside_container_flag_succeeds(
      self,
      mock_path,
      mock_config,
      mock_exec,
  ):
    expected_exception = "Expected Exception!"
    mock_config.return_value = None
    mock_exec.return_value = True
    mock_path.side_effect = Exception(expected_exception)

    with self.assertRaises(Exception) as raised_error:
      self.commands.invoke("test_command")
    self.assertEqual(
        raised_error.exception.args[0],
        expected_exception,
    )


class TestBuildDocs(CommandTestHarness):
  __test__ = True
  command = 'build-docs'


class TestBuildWheel(CommandTestHarness):
  __test__ = True
  command = 'build-wheel'


class TestFormatter(CommandTestHarness):
  __test__ = True
  command = 'fmt'


class TestLinter(CommandTestHarness):
  __test__ = True
  command = 'lint'


class TestSecTest(CommandTestHarness):
  __test__ = True
  command = 'sectest'


class TestTest(CommandTestHarness):
  __test__ = True
  command = 'test'


class TestTestWithOptions(CommandTestHarness):
  __test__ = True
  command = 'test'
  overload = (
      '-x',
      '/specific/file/to/test.py',
  )


class TestCoverage(CommandTestHarness):
  __test__ = True
  command = 'coverage'


class TestCoverageWithOptions(CommandTestHarness):
  __test__ = True
  command = 'coverage'
  overload = ('/specific/file/to/test.py',)


class TestReinstallRequirements(CommandTestHarness):
  __test__ = True
  command = 'reinstall-requirements'
