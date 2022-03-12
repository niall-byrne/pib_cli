"""Test the UserConfigurationVersionBase implementations."""

import os
from typing import Dict, List, Union
from unittest.mock import patch

from pib_cli import config
from pib_cli.config import yaml_keys

from .. import versions
from ..bases.fixtures import user_configuration_base_harness


@patch.dict(os.environ, {config.ENV_PROJECT_NAME: "test_value"})
class TestUserConfigurationV200(
    user_configuration_base_harness.UserConfigurationVersionBaseTestHarness
):
  """Test the UserConfigurationV200 class."""

  version = "2.0.0"
  mock_config: List[yaml_keys.TypeUserConfiguration]

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = versions.UserConfigurationV200

  def setUp(self) -> None:
    self.mock_config = self.mock_command_config

  def test_get_project_name(self) -> None:
    instance = self.create_instance()
    self.assertEqual(instance.project_name, "test_value")

  @patch.dict(os.environ, {}, clear=True)
  def test_get_project_name_unset(self) -> None:
    with self.assertRaises(KeyError):
      self.create_instance()


@patch.dict(os.environ, {config.ENV_PROJECT_NAME: "test_value"})
class TestUserConfigurationV210(
    user_configuration_base_harness.UserConfigurationVersionBaseTestHarness
):
  """Test the UserConfigurationV210 class."""

  version = "2.1.0"
  mock_config: Dict[str, Union[str, List[yaml_keys.TypeUserConfiguration]]]

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = versions.UserConfigurationV210

  def setUp(self) -> None:
    self.mock_config = {
        yaml_keys.V210_CLI_CONFIG_ROOT: self.mock_command_config,
    }

  def test_get_project_name(self) -> None:
    instance = self.create_instance()
    self.assertEqual(instance.project_name, "test_value")

  @patch.dict(os.environ, {}, clear=True)
  def test_get_project_name_config(self) -> None:
    self.mock_config[yaml_keys.V210_CLI_CONFIG_PROJECT_NAME] = "test_value_two"
    instance = self.create_instance()
    self.assertEqual(instance.project_name, "test_value_two")

  @patch.dict(os.environ, {}, clear=True)
  def test_get_project_name_unset(self) -> None:
    with self.assertRaises(KeyError):
      self.create_instance()
