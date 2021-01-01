"""Test the Intial Environment and Discovery Functions"""

import os
from unittest import TestCase
from unittest.mock import patch

from .. import check_project_name, config, get_config_file_name, project_root


class TestGetConfigFileName(TestCase):

  @patch.dict(
      os.environ,
      {},
      clear=True,
  )
  def test_no_override(self):
    result = get_config_file_name()
    assert result == os.path.join(project_root, "config", "config.yml")

  @patch.dict(
      os.environ,
      {config.ENV_OVERRIDE_CONFIG_LOCATION: "/app/somefile.yml"},
      clear=True,
  )
  def test_with_override(self):
    result = get_config_file_name()
    assert result == "/app/somefile.yml"


class TestCheckProjectName(TestCase):

  @patch.dict(
      os.environ,
      {config.ENV_PROJECT_NAME: "valid_value"},
      clear=True,
  )
  def test_check_project_name(self):
    check_project_name()

  @patch.dict(
      os.environ,
      {},
      clear=True,
  )
  def test_check_project_name_missing(self):
    with self.assertRaises(KeyError) as assertion_error:
      check_project_name()
    self.assertEqual(
        assertion_error.exception.args[0], config.ERROR_PROJECT_NAME_NOT_SET
    )
