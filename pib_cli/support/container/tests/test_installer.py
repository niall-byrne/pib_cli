"""Tests for the DevContainer class."""

from typing import List
from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.support import container
from pib_cli.support.container import installer
from pib_cli.support.iterators.bases import file_copy_base


class DevContainerTest(TestCase):
  """Tests for the DevContainer class."""

  def create_mock_source_destination(
      self, start: int, end: int
  ) -> List[file_copy_base.SourceDestinationPair]:
    results = []
    for index in range(start, end):
      results.append(
          file_copy_base.SourceDestinationPair(
              source=f"/source/file.{index}",
              destination=f"/destination/file.{index}"
          )
      )
    return results

  def setUp(self) -> None:
    self.instance = installer.DevContainerInstaller()

  def test_initialization(self) -> None:
    self.assertEqual(
        self.instance.bash_setup_success_message, "Setup Succeeded!"
    )

  def test_class_hierarchy(self) -> None:
    self.assertIsInstance(self.instance, container.DevContainer)

  @patch(
      installer.__name__ + ".container_bash_files.ContainerBashFilesIterator"
  )
  @patch(installer.__name__ + ".container_shim_file.ContainerShimFileIterator")
  def test_get_installation_files(
      self, m_iterator1: Mock, m_iterator2: Mock
  ) -> None:
    m_iterator1.return_value = self.create_mock_source_destination(0, 2)
    m_iterator2.return_value = self.create_mock_source_destination(2, 4)
    expected = m_iterator2.return_value + m_iterator1.return_value

    self.assertListEqual(
        self.instance.get_installation_files(),
        expected,
    )

  @patch("os.makedirs")
  @patch("shutil.copy")
  def test_setup(self, m_copy: Mock, m_makedirs: Mock) -> None:
    m_callback = Mock()
    m_installation_files = self.create_mock_source_destination(0, 1)

    with patch.object(
        self.instance,
        "get_installation_files",
        return_value=m_installation_files
    ):
      self.instance.setup(m_callback)

    m_makedirs.assert_called_once_with(
        self.instance.local_executable_folder, exist_ok=True
    )
    self.assertEqual(m_copy.call_count, len(m_installation_files))
    self.assertEqual(m_callback.call_count, len(m_installation_files) + 1)
    for mock_file in m_installation_files:
      m_copy.assert_any_call(mock_file.source, mock_file.destination)
      m_callback.assert_any_call(
          f"Copied: {mock_file.source} -> {mock_file.destination}"
      )
    m_callback.assert_any_call(self.instance.bash_setup_success_message)
