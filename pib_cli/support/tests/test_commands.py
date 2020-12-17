"""Tests for Command Invocations"""

from unittest import TestCase

import yaml
from pib_cli import config_filename
from pib_cli.support.commands import Commands
from pib_cli.support.paths import PathManager
from pib_cli.support.processes import ProcessManager
from .fixtures import CommandTestHarness


class TestPathManager(TestCase):

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


class TestBuildDocs(CommandTestHarness):
  __test__ = True
  command = 'build-docs'


class TestBuildWheel(CommandTestHarness):
  __test__ = True
  command = 'build-wheel'


class TestSecTest(CommandTestHarness):
  __test__ = True
  command = 'sectest'


class TestLinter(CommandTestHarness):
  __test__ = True
  command = 'lint'
