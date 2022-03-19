"""Tests for the UserConfigurationValidator class."""

from pathlib import Path
from unittest import TestCase, mock

from jsonschema import ValidationError
from pib_cli import config
from pib_cli.support import state
from pib_cli.support.mixins import json_file, yaml_file

from .. import validator


class TestUserConfigurationValidator(yaml_file.YAMLFileReader, TestCase):
  """Tests for the UserConfigurationValidator class."""

  def setUp(self) -> None:
    state.State.clear()
    state.State().load()

  @mock.patch(json_file.__name__ + ".JSONFileReader.load_json_file")
  def test_instantiation(self, _: mock.Mock) -> None:
    instance = validator.UserConfigurationValidator()
    self.assertDictEqual(
        instance.active_schemas, {
            "2.1.0": "cli_base_schema_v2.1.0.json",
            "2.0.0": "cli_cmd_schema_v0.1.0.json"
        }
    )

  @mock.patch(json_file.__name__ + ".JSONFileReader.load_json_file")
  def test_file_loading(self, m_json: mock.Mock) -> None:
    instance = validator.UserConfigurationValidator()
    self.assertDictEqual(
        instance.schemas, {
            "2.1.0": m_json.return_value,
            "2.0.0": m_json.return_value,
        }
    )
    m_json.assert_any_call(
        Path(config.__file__).parent / "schemas" /
        instance.active_schemas["2.1.0"]
    )
    m_json.assert_any_call(
        Path(config.__file__).parent / "schemas" /
        instance.active_schemas["2.0.0"]
    )

  @mock.patch(validator.__name__ + ".validate")
  @mock.patch(validator.__name__ + ".RefResolver")
  def test_validate_v210_valid(
      self, m_resolver: mock.Mock, m_validate: mock.Mock
  ) -> None:
    mock_object = mock.Mock()
    instance = validator.UserConfigurationValidator()
    version = instance.validate(mock_object)
    m_validate.assert_called_once_with(
        mock_object,
        instance.schemas["2.1.0"],
        resolver=m_resolver.return_value,
    )
    self.assertEqual(version, "2.1.0")

  @mock.patch(validator.__name__ + ".validate")
  @mock.patch(validator.__name__ + ".RefResolver")
  def test_validate_v200_valid(
      self, m_resolver: mock.Mock, m_validate: mock.Mock
  ) -> None:
    m_validate.side_effect = [ValidationError("MockValidationError"), None]
    mock_object = mock.Mock()
    instance = validator.UserConfigurationValidator()
    version = instance.validate(mock_object)
    m_validate.assert_any_call(
        mock_object,
        instance.schemas["2.1.0"],
        resolver=m_resolver.return_value,
    )
    m_validate.assert_any_call(
        mock_object,
        instance.schemas["2.0.0"],
        resolver=m_resolver.return_value,
    )
    self.assertEqual(m_validate.call_count, 2)
    self.assertEqual(version, "2.0.0")

  @mock.patch(validator.__name__ + ".validate")
  @mock.patch(validator.__name__ + ".RefResolver")
  def test_validate_none_valid(
      self, m_resolver: mock.Mock, m_validate: mock.Mock
  ) -> None:
    m_validate.side_effect = [
        ValidationError("MockValidationError"),
        ValidationError("MockValidationError")
    ]
    mock_object = mock.Mock()
    instance = validator.UserConfigurationValidator()
    with self.assertRaises(ValidationError):
      instance.validate(mock_object)
    m_validate.assert_any_call(
        mock_object,
        instance.schemas["2.1.0"],
        resolver=m_resolver.return_value,
    )
    m_validate.assert_any_call(
        mock_object,
        instance.schemas["2.0.0"],
        resolver=m_resolver.return_value,
    )
    self.assertEqual(m_validate.call_count, 2)

  def test_validate_default_config(self) -> None:
    valid_config_file = Path(config.__file__).parent / "default_cli_config.yml"
    valid_loaded_config = self.load_yaml_file(valid_config_file)
    instance = validator.UserConfigurationValidator()
    version = instance.validate(valid_loaded_config)
    self.assertEqual(version, "2.1.0")

  def test_validate_known_invalid_config(self) -> None:
    invalid_loaded_config = {
        "string": "value"
    }
    instance = validator.UserConfigurationValidator()
    with self.assertRaises(ValidationError):
      instance.validate(invalid_loaded_config)
