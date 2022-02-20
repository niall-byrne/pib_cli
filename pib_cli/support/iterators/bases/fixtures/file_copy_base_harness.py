"""Test harness for FileCopyIteratorBase subclasses."""

import abc
from typing import List, Type
from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.support.iterators.bases import file_copy_base


@patch(file_copy_base.__name__ + ".glob.glob")
class FileCopyIteratorBaseTestHarness(TestCase, abc.ABC):
  """Test harness for FileCopyIteratorBase subclasses."""

  __test__ = False
  test_class: Type[file_copy_base.FileCopyIteratorBase]
  expected_results: List[file_copy_base.SourceDestinationPair]

  def get_results(self) -> List[file_copy_base.SourceDestinationPair]:
    return list(self.test_class())

  def get_mock_glob_result(self) -> List[str]:
    return ["3", "2", "1"]

  def get_reverse_mock_glob_result(self) -> List[str]:
    result = self.get_mock_glob_result()
    result.reverse()
    return result

  def test_initialize(self, m_glob: Mock) -> None:
    m_glob.return_value = self.get_mock_glob_result()
    instance = self.test_class()
    m_glob.assert_called_once_with(self.test_class.glob_pattern)
    self.assertListEqual(instance.files, self.get_mock_glob_result())

  def test_hook_create_destination(self, m_glob: Mock) -> None:
    m_glob.return_value = self.get_mock_glob_result()
    instance = self.test_class()
    result = list(instance)
    expected = [
        file_copy_base.SourceDestinationPair(
            value,
            instance.hook_create_destination(value),
        ) for value in self.get_reverse_mock_glob_result()
    ]

    self.assertListEqual(
        result,
        expected,
    )

  def test_results(self, m_glob: Mock) -> None:
    m_glob.return_value = self.get_mock_glob_result()
    self.assertEqual(self.get_results(), self.expected_results)
