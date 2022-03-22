"""Test harness for the CommandSelectorBase class subclasses."""

import abc
from typing import Dict, List, Optional, Type, Union, cast
from unittest import TestCase
from unittest.mock import patch

from pib_cli.config import yaml_keys
from pib_cli.support import container
from pib_cli.support.container import exceptions

from .. import command_selector_base

TypeYamlConfig = Union[yaml_keys.TypeUserConfiguration,
                       yaml_keys.TypeLegacyUserConfiguration]


class CommandSelectorBaseTestHarness(TestCase, abc.ABC):
  """Test harness for the CommandSelectorBase class subclasses."""

  test_class: Type[command_selector_base.CommandSelectorBase]
  test_data: Dict[str, Union[List[str], str, bool]]

  def get_yaml_test_data(
      self,
      commands: Optional[Union[str, List[str]]] = None,
      container_only: Optional[bool] = None,
  ) -> TypeYamlConfig:
    test_data = self.test_data.copy()
    test_data.update(
        {yaml_keys.COMMANDS: commands if commands else ["default_command"]}
    )
    if container_only is not None:
      test_data.update({yaml_keys.CONTAINER_ONLY: container_only})
    return cast(
        TypeYamlConfig,
        test_data,
    )

  def create_patched_instance(
      self,
      selected_configuration: TypeYamlConfig,
      valid_container: bool,
  ) -> command_selector_base.CommandSelectorBase:
    with patch(
        command_selector_base.__name__ + ".container.DevContainer"
    ) as m_container:
      if not valid_container:
        valid = m_container.return_value.container_valid_exception
        valid.side_effect = exceptions.DevContainerException(
            "message", exit_code=1
        )
      return self.test_class(selected_configuration)

  def test_initialize(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.test_class(test_data)

    self.assertIsInstance(instance.container, container.DevContainer)
    self.assertEqual(instance.user_configuration, test_data)

  def test_initialize_str(self) -> None:
    test_data = self.get_yaml_test_data(
        commands="test_simple_string_command",
        container_only=True,
    )
    instance = self.test_class(test_data)

    self.assertIsInstance(instance.container, container.DevContainer)
    self.assertEqual(instance.user_configuration, test_data)

  def test_inside_container_is_config_executable(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.create_patched_instance(test_data, valid_container=True)

    instance.is_executable_exception()

  def test_outside_container_is_config_executable(self) -> None:
    test_data = self.get_yaml_test_data(container_only=True)
    instance = self.create_patched_instance(test_data, valid_container=False)

    with self.assertRaises(exceptions.DevContainerException):
      instance.is_executable_exception()

  def test_outside_container_is_config_executable_default(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.create_patched_instance(test_data, valid_container=False)

    instance.is_executable_exception()

  @abc.abstractmethod
  def test_get_config_path_method(self) -> None:
    """Override to test the get_config_path_method call."""

  def test_get_config_commands(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.test_class(test_data)

    self.assertEqual(
        instance.get_config_commands(),
        test_data['commands'],
    )

  def test_get_config_response_exit_code_zero(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.test_class(test_data)

    self.assertEqual(
        instance.get_config_response(0),
        test_data['success'],
    )

  def test_get_config_response_exit_code_non_zero(self) -> None:
    test_data = self.get_yaml_test_data()
    instance = self.test_class(test_data)

    self.assertEqual(
        instance.get_config_response(99),
        test_data['failure'],
    )
