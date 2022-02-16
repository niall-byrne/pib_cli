"""Test the YAMLFile mixin classes."""

import io
from unittest import TestCase, mock

import yaml

from .. import yaml_file

YAML_FILE_MODULE = yaml_file.__name__


@mock.patch(YAML_FILE_MODULE + '.yaml')
@mock.patch('builtins.open')
class YAMLFileReaderTest(TestCase):
  """Test the YAMLFileReader mixin class."""

  def setUp(self) -> None:
    self.instance = yaml_file.YAMLFileReader()
    self.virtual_file_handle = io.StringIO()
    self.mock_object = {
        "mock": "object"
    }
    self.mock_yaml = yaml.dump(self.mock_object, self.virtual_file_handle)
    self.mock_context = mock.Mock()

  def test_load_yaml_file_return_value(
      self,
      m_open: mock.Mock,
      m_yaml: mock.Mock,
  ) -> None:
    mock_path = "/mock/path"
    self.mock_context.return_value = self.mock_yaml
    m_open.return_value.__enter__.return_value = self.mock_context
    m_yaml.safe_load.return_value = self.mock_object

    result = self.instance.load_yaml_file(mock_path)
    self.assertEqual(result, self.mock_object)

  def test_load_json_file_call(
      self,
      m_open: mock.Mock,
      m_yaml: mock.Mock,
  ) -> None:
    mock_path = "/mock/path"
    self.mock_context.return_value = self.mock_yaml
    m_open.return_value.__enter__.return_value = self.mock_context

    self.instance.load_yaml_file(mock_path)
    m_yaml.safe_load.assert_called_once_with(self.mock_context)
