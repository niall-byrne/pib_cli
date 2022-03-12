"""Tests for the UserConfigurationFile class."""

import os
import pathlib
from typing import Optional
from unittest import TestCase
from unittest.mock import Mock, call, patch

import pib_cli
from pib_cli import config
from pib_cli.support.user_configuration import user_configuration_file, versions
from pib_cli.support.user_configuration.bases import user_configuration_base


class TestUserConfigurationFile(TestCase):
  """Tests for the UserConfigurationFile class."""

  def create_instance(
      self,
      file_name: Optional[str] = None
  ) -> user_configuration_file.UserConfigurationFile:
    return user_configuration_file.UserConfigurationFile(config_file=file_name)

  def test_initialize(self,) -> None:
    instance = self.create_instance()

    self.assertEqual(
        pathlib.Path(instance.git_root_folder),
        pathlib.Path(pib_cli.__file__).parent.parent.absolute(),
    )
    self.assertEqual(
        instance.project_root,
        pathlib.Path(pib_cli.__file__).parent.absolute(),
    )
    self.assertEqual(
        instance.default_config,
        os.path.join(instance.project_root, "config", "default_cli_config.yml"),
    )
    self.assertListEqual(
        instance.supported_versions,
        [versions.UserConfigurationV210, versions.UserConfigurationV200]
    )
    self.assertIsNone(instance.specified_file_name)

  def test_initialize_with_file(self,) -> None:
    instance = self.create_instance("mock_file")

    self.assertEqual(
        instance.specified_file_name,
        "mock_file",
    )

  @patch.dict(os.environ, {config.ENV_OVERRIDE_CONFIG_LOCATION: "/some_path"})
  def test_get_config_file_name_specified(self) -> None:

    mock_file_name = "./file.yml"

    instance = self.create_instance(file_name=mock_file_name)
    result = instance.get_config_file_name()

    self.assertEqual(
        result,
        str(pathlib.Path(mock_file_name).resolve()),
    )

  @patch.dict(os.environ, {config.ENV_OVERRIDE_CONFIG_LOCATION: "/some_path"})
  @patch(user_configuration_file.__name__ + ".path_map.PathMap")
  @patch(user_configuration_file.__name__ + ".os.path.exists")
  def test_get_config_file_name_env(
      self,
      m_exists: Mock,
      m_path_map: Mock,
  ) -> None:
    m_exists.side_effect = [True]
    m_path_map.return_value.git_root_folder = "/mock_path"

    instance = self.create_instance()
    result = instance.get_config_file_name()

    m_exists.assert_called_once_with("/some_path")
    self.assertEqual(result, "/some_path")

  @patch.dict(os.environ, {config.ENV_OVERRIDE_CONFIG_LOCATION: "/some_path"})
  @patch(user_configuration_file.__name__ + ".path_map.PathMap")
  @patch(user_configuration_file.__name__ + ".os.path.exists")
  def test_get_config_file_current_directory(
      self,
      m_exists: Mock,
      m_path_map: Mock,
  ) -> None:
    m_exists.side_effect = [False, True]
    m_path_map.return_value.git_root_folder = "/mock_path"

    instance = self.create_instance()
    result = instance.get_config_file_name()

    m_exists.assert_has_calls(
        [
            call("/some_path"),
            call(
                os.path.join(
                    m_path_map.return_value.git_root_folder,
                    config.PIB_CONFIG_FILE_NAME
                )
            )
        ]
    )

    self.assertEqual(
        result,
        os.path.join(
            m_path_map.return_value.git_root_folder, config.PIB_CONFIG_FILE_NAME
        ),
    )

  @patch.dict(os.environ, {}, clear=True)
  @patch(user_configuration_file.__name__ + ".path_map.PathMap")
  @patch(user_configuration_file.__name__ + ".os.path.exists")
  def test_get_config_file_default(
      self,
      m_exists: Mock,
      m_path_map: Mock,
  ) -> None:
    m_exists.side_effect = [False]
    m_path_map.return_value.git_root_folder = "/mock_path"

    instance = self.create_instance()
    result = instance.get_config_file_name()

    m_exists.assert_has_calls(
        [
            call(
                os.path.join(
                    m_path_map.return_value.git_root_folder,
                    config.PIB_CONFIG_FILE_NAME
                )
            )
        ]
    )

    self.assertEqual(
        result,
        instance.default_config,
    )

  @patch(
      user_configuration_file.__name__ + ".UserConfigurationFile.load_text_file"
  )
  def test_get_raw_file(
      self,
      m_text: Mock,
  ) -> None:
    m_text.return_value = " mock text content "
    instance = self.create_instance()
    self.assertEqual(instance.get_raw_file(), m_text.return_value.rstrip())

  @patch(
      user_configuration_file.__name__ + ".UserConfigurationFile.load_yaml_file"
  )
  @patch(
      user_configuration_file.__name__ + ".validator.UserConfigurationValidator"
  )
  def test_parse_version_valid(
      self,
      m_validator: Mock,
      m_yaml: Mock,
  ) -> None:
    m_validator.return_value.validate.return_value = "2.0.0"

    instance = self.create_instance()

    with patch.object(instance, "get_config_file_name") as m_get_config:
      result = instance.parse()

    m_yaml.assert_called_once_with(m_get_config.return_value)
    m_validator.assert_called_once_with()
    m_validator.return_value.validate.assert_called_once_with(
        m_yaml.return_value
    )
    self.assertIsInstance(
        result, user_configuration_base.UserConfigurationVersionBase
    )
    self.assertEqual(
        result.version,
        m_validator.return_value.validate.return_value,
    )

  @patch(
      user_configuration_file.__name__ + ".UserConfigurationFile.load_yaml_file"
  )
  @patch(
      user_configuration_file.__name__ + ".validator.UserConfigurationValidator"
  )
  def test_parse_version_invalid(
      self,
      m_validator: Mock,
      m_yaml: Mock,
  ) -> None:
    m_validator.return_value.version = "unknown"

    instance = self.create_instance()

    with patch.object(instance, "get_config_file_name") as m_get_config:
      with self.assertRaises(NotImplementedError):
        instance.parse()

    m_yaml.assert_called_once_with(m_get_config.return_value)
    m_validator.assert_called_once_with()
    m_validator.return_value.validate.assert_called_once_with(
        m_yaml.return_value
    )
