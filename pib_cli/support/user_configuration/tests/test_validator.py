"""Tests for the UserConfigurationValidator class."""

from pathlib import Path
from unittest import TestCase, mock

from jsonschema import ValidationError
from pib_cli import config
from pib_cli.support.mixins import json_file, yaml_file

from .. import validator


class TestUserConfigurationValidator(yaml_file.YAMLFileReader, TestCase):
  """Tests for the UserConfigurationValidator class."""

  @mock.patch(json_file.__name__ + ".JSONFileReader.load_json_file")
  def test_instantiation(self, m_json: mock.Mock) -> None:
    instance = validator.UserConfigurationValidator()
    self.assertEqual(
        instance.schema,
        m_json.return_value,
    )

  @mock.patch(json_file.__name__ + ".JSONFileReader.load_json_file")
  def test_file_loading(self, m_json: mock.Mock) -> None:
    instance = validator.UserConfigurationValidator()
    m_json.assert_called_once_with(instance.schema_file)

  @mock.patch(validator.__name__ + ".validate")
  def test_validate_call(self, m_validate: mock.Mock) -> None:
    mock_object = mock.Mock()
    instance = validator.UserConfigurationValidator()
    instance.validate(mock_object)
    m_validate.assert_called_once_with(mock_object, instance.schema)

  def test_validate_valid(self) -> None:
    valid_config_file = Path(config.__file__).parent / "config.yml"
    valid_loaded_config = self.load_yaml_file(valid_config_file)
    instance = validator.UserConfigurationValidator()
    instance.validate(valid_loaded_config)

  def test_validate_invalid(self) -> None:
    invalid_loaded_config = {
        "string": "value"
    }
    instance = validator.UserConfigurationValidator()
    with self.assertRaises(ValidationError):
      instance.validate(invalid_loaded_config)
