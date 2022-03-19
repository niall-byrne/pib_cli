"""Tests for the ContainerBashFilesIterator class."""

import os
from pathlib import Path

import pib_cli
from pib_cli.support.iterators.bases.file_copy_base import SourceDestinationPair
from pib_cli.support.iterators.bases.fixtures.file_copy_base_harness import (
    FileCopyIteratorBaseTestHarness,
)

from .. import container_bash_files


class TestContainerBashFilesIterator(FileCopyIteratorBaseTestHarness):
  """Tests for the ContainerBashFilesIterator class."""

  __test__ = True
  expected_results = [
      SourceDestinationPair(
          '1', str((Path.home() / Path('.1').name).resolve())
      ),
      SourceDestinationPair(
          '2', str((Path.home() / Path('.2').name).resolve())
      ),
      SourceDestinationPair(
          '3', str((Path.home() / Path('.3').name).resolve())
      ),
  ]

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = container_bash_files.ContainerBashFilesIterator

  def test_glob(self) -> None:
    self.assertEqual(
        self.test_class.glob_pattern,
        os.path.join(Path(pib_cli.__file__).parent, "bash", "bash*")
    )
