"""Test the Initial Environment and Discovery Functions."""

import os
from unittest import TestCase
from unittest.mock import Mock, patch

from .. import check_project_name, config, get_config_file_name, project_root


class TestGetConfigFileName(TestCase):
  """Test the get_config_file_name function."""

  @patch.dict(
      os.environ,
      {},
      clear=True,
  )
  def test_no_override(self) -> None:
    result = get_config_file_name()
    self.assertEqual(result, os.path.join(project_root, "config", "config.yml"))

  @patch.dict(
      os.environ,
      {config.ENV_OVERRIDE_CONFIG_LOCATION: "/app/somefile.yml"},
      clear=True,
  )
  @patch("os.path.exists", Mock(return_value=True))
  def test_with_override_exists(self) -> None:
    result = get_config_file_name()
    self.assertEqual(
        result,
        "/app/somefile.yml",
    )

  @patch.dict(
      os.environ,
      {config.ENV_OVERRIDE_CONFIG_LOCATION: "/app/somefile.yml"},
      clear=True,
  )
  @patch("os.path.exists", Mock(return_value=False))
  def test_with_override_does_not_exist(self) -> None:
    result = get_config_file_name()
    self.assertEqual(result, os.path.join(project_root, "config", "config.yml"))


class TestCheckProjectName(TestCase):
  """Test the check_project_name function."""

  @patch.dict(
      os.environ,
      {config.ENV_PROJECT_NAME: "valid_value"},
      clear=True,
  )
  def test_check_project_name(self) -> None:
    check_project_name()

  @patch.dict(
      os.environ,
      {},
      clear=True,
  )
  def test_check_project_name_missing(self) -> None:
    with self.assertRaises(KeyError) as assertion_error:
      check_project_name()
    self.assertEqual(
        assertion_error.exception.args[0], config.ERROR_PROJECT_NAME_NOT_SET
    )
