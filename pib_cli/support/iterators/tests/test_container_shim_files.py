"""Tests for the ContainerShimFileIterator class."""

import os

from pib_cli import project_root
from pib_cli.support import container
from pib_cli.support.iterators.bases.file_copy_base import SourceDestinationPair
from pib_cli.support.iterators.bases.fixtures.file_copy_base_harness import (
    FileCopyIteratorBaseTestHarness,
)

from .. import container_shim_file


class TestContainerShimFileIterator(FileCopyIteratorBaseTestHarness):
  """Tests for the ContainerShimFileIterator class."""

  __test__ = True
  expected_results = [
      SourceDestinationPair(
          '1',
          os.path.join(container.DevContainer.local_executable_folder, 'dev')
      ),
      SourceDestinationPair(
          '2',
          os.path.join(container.DevContainer.local_executable_folder, 'dev')
      ),
      SourceDestinationPair(
          '3',
          os.path.join(container.DevContainer.local_executable_folder, 'dev')
      ),
  ]

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = container_shim_file.ContainerShimFileIterator

  def test_glob(self) -> None:
    self.assertEqual(
        self.test_class.glob_pattern,
        os.path.join(project_root, "bash", "shim")
    )
