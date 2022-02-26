"""Tests for the DevContainerBase class."""

import os
from pathlib import Path
from unittest import TestCase

from pib_cli import config
from pib_cli.support import container
from pib_cli.support.mixins import text_file


class DevContainerBaseTest(TestCase):
  """Tests for the DevContainerBase class."""

  def setUp(self) -> None:
    self.instance = container.DevContainer()

  def test_class_hierarchy(self) -> None:
    self.assertIsInstance(self.instance, text_file.TextFileReader)

  def test_initialization(self) -> None:
    self.assertEqual(
        self.instance.file_container_marker,
        os.path.join("/", "etc", "container_release")
    )
    self.assertEqual(
        self.instance.file_version_marker,
        os.path.join("/", "etc", "container_pib_version")
    )
    self.assertEqual(
        self.instance.local_executable_folder,
        str((Path.home() / ".local/bin").resolve())
    )
    self.assertEqual(self.instance.minimum_pib_version, "1.0.0")
    self.assertEqual(self.instance.unversioned_pib_value, "0.0.1")
    self.assertEqual(
        self.instance.incompatible_container_exit_code,
        config.EXIT_CODE_CONTAINER_INCOMPATIBLE
    )
