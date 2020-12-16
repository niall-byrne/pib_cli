"""Tests for the CLI Utilities"""

from unittest import TestCase

from pib_cli.support.cli_utilities import Utilities
from pib_cli.support.paths import PathManager
from pib_cli.support.processes import ProcessManager


class TestPathManager(TestCase):

  def setUp(self):
    self.utils = Utilities()

  def test_initial_instance_variables(self):
    self.assertIsInstance(self.utils.process_manager, ProcessManager)
    self.assertIsInstance(self.utils.path_manager, PathManager)
