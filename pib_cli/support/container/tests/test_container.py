"""Tests for the DevContainer class."""

from unittest import TestCase
from unittest.mock import patch

from pib_cli import config
from pib_cli.support import container
from pib_cli.support.container import exceptions
from pib_cli.support.container.bases import container as container_base


class DevContainerTest(TestCase):
  """Tests for the DevContainer class."""

  def check_exception(
      self, exc: exceptions.DevContainerException, message: str
  ) -> None:
    self.assertEqual(exc.args, (message,))

  def setUp(self) -> None:
    self.instance = container.DevContainer()

  def test_class_hierarchy(self) -> None:
    self.assertIsInstance(self.instance, container_base.DevContainerBase)

  def test_container_only_exception(self) -> None:
    with self.assertRaises(exceptions.DevContainerException) as exc:
      self.instance.container_only_exception()
      self.check_exception(
          exc.exception,
          config.ERROR_CONTAINER_ONLY,
      )

  def test_container_version_exception(self) -> None:
    with self.assertRaises(exceptions.DevContainerException) as exc:
      self.instance.container_version_exception()
      self.check_exception(
          exc.exception,
          config.ERROR_CONTAINER_VERSION(self.instance.minimum_pib_version)
      )

  def test_is_container_true(self) -> None:
    with patch("os.path.exists", return_value=True) as m_os:
      self.assertTrue(self.instance.is_container())
      m_os.assert_called_once_with(self.instance.file_container_marker)

  def test_is_container_false(self) -> None:
    with patch("os.path.exists", return_value=False) as m_os:
      self.assertFalse(self.instance.is_container())
      m_os.assert_called_once_with(self.instance.file_container_marker)

  def test_is_compatible_container_true(self) -> None:
    with patch.object(
        self.instance, "load_text_file", return_value="1.0.0\n"
    ) as m_load:
      self.assertTrue(self.instance.is_compatible_container())
      m_load.assert_called_once_with(self.instance.file_version_marker)

  def test_is_compatible_container_false(self) -> None:
    with patch.object(
        self.instance, "load_text_file", return_value="0.9.0\n"
    ) as m_load:
      self.assertFalse(self.instance.is_compatible_container())
      m_load.assert_called_once_with(self.instance.file_version_marker)

  def test_is_compatible_container_file_not_found(self) -> None:
    with patch.object(
        self.instance, "load_text_file", side_effect=FileNotFoundError
    ) as m_load:
      self.assertFalse(self.instance.is_compatible_container())
      m_load.assert_called_once_with(self.instance.file_version_marker)

  def test_assert_valid_container(self) -> None:
    with patch("os.path.exists", return_value=True):
      with patch.object(
          self.instance, "load_text_file", return_value="1.0.1\n"
      ):
        self.instance.container_valid_exception()

  def test_assert_valid_container_not_container(self) -> None:
    with patch("os.path.exists", return_value=False):
      with patch.object(
          self.instance, "load_text_file", return_value="0.9.0\n"
      ):
        with self.assertRaises(exceptions.DevContainerException) as exc:
          self.instance.container_valid_exception()
          self.check_exception(
              exc.exception,
              config.ERROR_CONTAINER_ONLY,
          )

  def test_assert_valid_container_wrong_version(self) -> None:
    with patch("os.path.exists", return_value=True):
      with patch.object(
          self.instance, "load_text_file", return_value="0.9.0\n"
      ):
        with self.assertRaises(exceptions.DevContainerException) as exc:
          self.instance.container_valid_exception()
          self.check_exception(
              exc.exception,
              config.ERROR_CONTAINER_VERSION(self.instance.minimum_pib_version)
          )
