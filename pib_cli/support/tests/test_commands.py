"""Tests for Command Invocations"""

from unittest import TestCase

import yaml
from pib_cli import config_filename
from pib_cli.support.commands import Commands
from pib_cli.support.paths import PathManager
from pib_cli.support.processes import ProcessManager
from .fixtures import CommandTestHarness


class TestCommandClass(TestCase):

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

  def test_container_only_flag_true(self):
    path_method = 'non_existent'
    test_command = 'test_command'
    self.config.append({
        'name': test_command,
        'container_only': True,
        'path_method': path_method
    })
    self.commands.config = self.config

    response = self.commands.invoke(test_command)
    assert response == self.commands.container_only_error

  def test_container_only_flag_false(self):
    path_method = 'non_existent'
    test_command = 'test_command'
    self.config.append({'name': test_command, 'path_method': path_method})
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
