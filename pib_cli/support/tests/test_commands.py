"""Tests for Command Invocations"""

import glob
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import patchbay
import yaml
from pib_cli import config_filename, project_root
from pib_cli.support.commands import Commands
from pib_cli.support.paths import PathManager
from pib_cli.support.processes import ProcessManager
from .. import yaml_keys
from .fixtures import CommandTestHarness


class TestCommandClass(TestCase):

  def yaml_test_data(self, path_method, test_command, container_only):
    return {
        yaml_keys.COMMAND_NAME: test_command,
        yaml_keys.CONTAINER_ONLY: container_only,
        yaml_keys.PATH_METHOD: path_method
    }

  def setUp(self):
    self.commands = Commands()
    with open(config_filename) as file_handle:
      self.config = yaml.safe_load(file_handle)

  def test_initial_instance_variables(self):
    self.assertIsInstance(self.commands.process_manager, ProcessManager)
    self.assertIsInstance(self.commands.path_manager, PathManager)
    self.assertIsInstance(self.commands.config, list)
    self.assertListEqual(self.config, self.commands.config)

  def test_invoke_non_existent_command(self):
    with self.assertRaises(KeyError):
      self.commands.invoke("non-existent-command")

  def test_invoke_non_existent_command_with_options(self):
    with self.assertRaises(KeyError):
      self.commands.invoke("non-existent-command", overload=('option1',))

  def test_coerce_from_string_with_string(self):
    test_value = "Hello"
    self.assertEqual(
        self.commands.coerce_from_string_to_list(test_value),
        [test_value],
    )

  def test_coerce_from_string_with_iterable(self):
    test_value = ["Hello"]
    self.assertEqual(
        self.commands.coerce_from_string_to_list(test_value),
        test_value,
    )

  @patch(patchbay.COMMANDS_IS_CONTAINER)
  def test_outside_container_flag_true(self, mock_container):
    mock_container.return_value = False
    path_method = 'non_existent'
    test_command = 'test_command'
    self.config.append(self.yaml_test_data(path_method, test_command, True))
    self.commands.config = self.config

    response = self.commands.invoke(test_command)
    self.assertEqual(response, self.commands.container_only_error)
    self.assertEqual(0, self.commands.process_manager.exit_code)

  @patch(patchbay.COMMANDS_IS_CONTAINER)
  def test_outside_container_flag_false(self, mock_container):
    mock_container.return_value = False
    path_method = 'non_existent'
    test_command = 'test_command'
    test_config = self.yaml_test_data(path_method, test_command, True)
    del test_config[yaml_keys.CONTAINER_ONLY]
    self.config.append(test_config)
    self.commands.config = self.config

    with self.assertRaises(AttributeError) as asserted_exception:
      self.commands.invoke(test_command)
    self.assertEqual(
        asserted_exception.exception.args[0],
        "'PathManager' object has no attribute '%s'" % path_method,
    )
    self.assertIsNone(self.commands.process_manager.exit_code)

  @patch(patchbay.COMMANDS_IS_CONTAINER)
  def test_outside_container_flag_missing(self, mock_container):
    mock_container.return_value = False
    path_method = 'non_existent'
    test_command = 'test_command'
    self.config.append(self.yaml_test_data(path_method, test_command, False))
    self.commands.config = self.config

    with self.assertRaises(AttributeError) as asserted_exception:
      self.commands.invoke(test_command)
    self.assertEqual(
        asserted_exception.exception.args[0],
        "'PathManager' object has no attribute '%s'" % path_method,
    )
    self.assertIsNone(self.commands.process_manager.exit_code)

  @patch(patchbay.COMMANDS_OS_PATH_EXISTS)
  def test_is_container_true(self, mock_exists):
    mock_exists.return_value = True
    result = self.commands.is_container()
    mock_exists.assert_called_once_with(self.commands.container_marker)
    self.assertTrue(result)

  @patch(patchbay.COMMANDS_OS_PATH_EXISTS)
  def test_is_container_false(self, mock_exists):
    mock_exists.return_value = False
    result = self.commands.is_container()
    mock_exists.assert_called_once_with(self.commands.container_marker)
    self.assertFalse(result)

  @patch(patchbay.COMMANDS_SHUTIL_COPY)
  @patch(patchbay.COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_copy_operations(self, mock_exists, mock_copy):
    mock_exists.return_value = True
    self.commands.setup_bash()
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    for file_name in bash_files:
      mock_copy.assert_any_call(file_name, str(Path.home()))
    self.assertEqual(len(bash_files), mock_copy.call_count)

  @patch(patchbay.COMMANDS_SHUTIL_COPY)
  @patch(patchbay.COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_output(self, mock_exists, _):
    mock_exists.return_value = True
    result = self.commands.setup_bash()
    home_dir = str(Path.home())
    expected_results = []
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    for file_name in bash_files:
      expected_results.append(f"Copied: {file_name} -> {home_dir} ")
    expected_results.append(Commands.setup_bash_success)
    self.assertEqual(result, "\n".join(expected_results))

  @patch(patchbay.COMMANDS_SHUTIL_COPY)
  @patch(patchbay.COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_outside_container(self, mock_exists, mock_copy):
    mock_exists.return_value = False
    results = self.commands.setup_bash()
    mock_copy.assert_not_called()
    self.assertEqual(results, Commands.container_only_error)


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
