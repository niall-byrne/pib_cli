"""Tests for the UserConfiguration class."""

import abc
from typing import Any, List, Type
from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.config import yaml_keys

from .. import user_configuration_base


class UserConfigurationVersionBaseTestHarness(TestCase, abc.ABC):
  """Test harness for the UserConfigurationVersionBase class."""

  test_class: Type[user_configuration_base.UserConfigurationVersionBase]
  version: str
  mock_config: Any
  mock_command_config: List[yaml_keys.TypeUserConfiguration] = [
      {
          yaml_keys.COMMAND_NAME: "command1",
          yaml_keys.COMMANDS: ["/bin/command1"]
      },
      {
          yaml_keys.COMMAND_NAME: "command2",
          yaml_keys.COMMANDS: ["/bin/command2"]
      },
      {
          yaml_keys.COMMAND_NAME: "command3",
          yaml_keys.COMMANDS: ["/bin/command3"]
      },
  ]

  def create_instance(
      self
  ) -> user_configuration_base.UserConfigurationVersionBase:
    return self.test_class(self.mock_config)

  def test_initialize(self,) -> None:
    instance = self.create_instance()

    self.assertEqual(instance.configuration, self.mock_config)
    self.assertIsInstance(
        instance.configuration_command_index,
        dict,
    )
    self.assertEqual(instance.version, self.version)

  def test_initialize_configuration_command_index(self,) -> None:
    expected_result = {}
    instance = self.create_instance()

    for command in self.mock_command_config:
      expected_result[command[yaml_keys.COMMAND_NAME]] = command

    self.assertDictEqual(
        instance.configuration_command_index,
        expected_result,
    )

  def test_get_command_definitions(self,) -> None:
    instance = self.create_instance()
    self.assertEqual(
        instance.get_command_definitions(),
        self.mock_command_config,
    )

  @patch(
      user_configuration_base.__name__ +
      ".selected.SelectedUserConfigurationEntry"
  )
  def test_select_config_entry_found(
      self,
      m_selected: Mock,
  ) -> None:
    index = 2
    instance = self.create_instance()

    found = instance.select_config_entry(
        self.mock_command_config[index][yaml_keys.COMMAND_NAME]
    )

    self.assertEqual(found, m_selected.return_value)
    m_selected.assert_called_once_with(self.mock_command_config[index])

  @patch(
      user_configuration_base.__name__ +
      ".selected.SelectedUserConfigurationEntry"
  )
  def test_select_config_entry_not_found(
      self,
      _: Mock,
  ) -> None:
    mock_command = "non_existent_command"
    instance = self.create_instance()

    with self.assertRaises(KeyError) as exc:
      instance.select_config_entry(mock_command)
    self.assertEqual(
        exc.exception.args,
        ("Could not find command named: %s" % mock_command,)
    )

  @abc.abstractmethod
  def test_get_project_name(self) -> None:
    """Override to test the get_project_name_method."""
