"""Tests for the UserConfiguration class."""

from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.config import yaml_keys
from pib_cli.support import user_configuration
from pib_cli.support.user_configuration import validator


@patch(user_configuration.__name__ + ".UserConfiguration.load_yaml_file")
@patch(user_configuration.__name__ + ".selected.SelectedUserConfigurationEntry")
class TestUserConfigurationYamlMethods(TestCase):
  """Tests for the UserConfiguration class relating to YAML."""

  def create_instance(self) -> user_configuration.UserConfiguration:
    return user_configuration.UserConfiguration()

  def setUp(self) -> None:
    self.mock_config = [
        {
            yaml_keys.COMMAND_NAME: "command1",
            yaml_keys.COMMANDS: "/bin/command1"
        },
        {
            yaml_keys.COMMAND_NAME: "command2",
            yaml_keys.COMMANDS: "/bin/command2"
        },
        {
            yaml_keys.COMMAND_NAME: "command3",
            yaml_keys.COMMANDS: "/bin/command3"
        },
    ]

  def test_initialize(
      self,
      _: Mock,
      m_yaml: Mock,
  ) -> None:
    m_yaml.return_value = self.mock_config
    instance = self.create_instance()

    self.assertEqual(instance.configuration, m_yaml.return_value)
    self.assertIsInstance(
        instance.configuration_validator, validator.UserConfigurationValidator
    )

  def test_initialize_configuration_command_index(
      self,
      _: Mock,
      m_yaml: Mock,
  ) -> None:
    m_yaml.return_value = self.mock_config
    expected_result = {}
    instance = self.create_instance()

    for command in self.mock_config:
      expected_result[command[yaml_keys.COMMAND_NAME]] = command

    self.assertDictEqual(
        instance.configuration_command_index,
        expected_result,
    )

  def test_select_config_entry_found(
      self,
      m_selected: Mock,
      m_yaml: Mock,
  ) -> None:
    index = 2
    m_yaml.return_value = self.mock_config
    instance = self.create_instance()

    found = instance.select_config_entry(
        self.mock_config[index][yaml_keys.COMMAND_NAME]
    )

    self.assertEqual(found, m_selected.return_value)
    m_selected.assert_called_once_with(self.mock_config[index])

  def test_select_config_entry_not_found(
      self,
      _: Mock,
      m_yaml: Mock,
  ) -> None:
    mock_command = "non_existent_command"
    m_yaml.return_value = self.mock_config
    instance = self.create_instance()

    with self.assertRaises(KeyError) as exc:
      instance.select_config_entry(mock_command)
    self.assertEqual(
        exc.exception.args,
        ("Could not find command named: %s" % mock_command,)
    )

  @patch(user_configuration.__name__ + ".validator.UserConfigurationValidator")
  def test_validate(
      self,
      m_validator: Mock,
      _: Mock,
      m_yaml: Mock,
  ) -> None:
    instance = self.create_instance()
    instance.validate()

    m_validator.assert_called_once_with()
    m_validator.return_value.validate.assert_called_once_with(
        m_yaml.return_value
    )


class TestUserConfigurationTextMethods(TestCase):
  """Tests for the UserConfiguration class relating to plain text."""

  def create_instance(self) -> user_configuration.UserConfiguration:
    with patch(
        user_configuration.__name__ + ".validator.UserConfigurationValidator"
    ):
      with patch(
          user_configuration.__name__ + ".UserConfiguration.load_yaml_file"
      ):
        return user_configuration.UserConfiguration()

  def setUp(self) -> None:
    self.instance = self.create_instance()

  @patch(user_configuration.__name__ + ".UserConfiguration.load_text_file")
  def test_get_raw_file(
      self,
      m_text: Mock,
  ) -> None:
    m_text.return_value = " mock text content "
    instance = self.create_instance()
    self.assertEqual(instance.get_raw_file(), m_text.return_value.rstrip())