"""Tests for External Command Invocations"""

import glob
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from ... import config, patchbay, project_root
from ..internal_commands import setup_bash


class TestSetupBash(TestCase):

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_copy_operations(self, mock_exists, mock_copy):
    mock_exists.return_value = True
    setup_bash()
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    for file_name in bash_files:
      mock_copy.assert_any_call(file_name, str(Path.home()))
    self.assertEqual(len(bash_files), mock_copy.call_count)

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_output(self, mock_exists, _):
    mock_exists.return_value = True
    result = setup_bash()
    home_dir = str(Path.home())
    expected_results = []
    bash_files = glob.glob(os.path.join(project_root, "bash", ".*"))
    for file_name in bash_files:
      expected_results.append(f"Copied: {file_name} -> {home_dir} ")
    expected_results.append(config.SETTING_BASH_SETUP_SUCCESS_MESSAGE)
    self.assertEqual(result, "\n".join(expected_results))

  @patch(patchbay.INTERNAL_COMMANDS_SHUTIL_COPY)
  @patch(patchbay.INTERNAL_COMMANDS_OS_PATH_EXISTS)
  def test_setup_bash_outside_container(self, mock_exists, mock_copy):
    mock_exists.return_value = False
    results = setup_bash()
    mock_copy.assert_not_called()
    self.assertEqual(results, config.ERROR_CONTAINER_ONLY)
