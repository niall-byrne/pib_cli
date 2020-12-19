"""Test the Configuration File"""

import os
from unittest import TestCase
from unittest.mock import patch

from .. import config, get_config_file_name, project_root


class TestGetConfigFileName(TestCase):

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
