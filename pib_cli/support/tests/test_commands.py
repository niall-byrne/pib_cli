"""Tests for Command Invocations"""

from unittest import TestCase
from unittest.mock import patch

import yaml
from pib_cli import config_filename
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
    assert self.commands.coerce_from_string_to_list(test_value) == [test_value]

  def test_coerce_from_string_with_iterable(self):
    test_value = ["Hello"]
    assert self.commands.coerce_from_string_to_list(test_value) == test_value

  @patch('pib_cli.support.commands.PathManager.is_container')
  def test_container_only_flag_true(self, mock_container):
    mock_container.return_value = False
    path_method = 'non_existent'
    test_command = 'test_command'
    self.config.append(self.yaml_test_data(path_method, test_command, True))
    self.commands.config = self.config

    response = self.commands.invoke(test_command)
    assert response == self.commands.container_only_error

  @patch('pib_cli.support.commands.PathManager.is_container')
  def test_container_only_flag_false(self, mock_container):
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

  @patch('pib_cli.support.commands.PathManager.is_container')
  def test_container_only_flag_missing(self, mock_container):
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


class TestSetupPython(CommandTestHarness):
  __test__ = True
  command = 'setup-bash'
