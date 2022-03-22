"""Tests for the CustomClickCommandIterator class."""

from contextlib import ExitStack
from typing import List, Tuple
from unittest import TestCase
from unittest.mock import patch

import click
from click.testing import CliRunner
from pib_cli.config import yaml_keys
from pib_cli.support import state
from pib_cli.support.user_configuration.bases import version_base

from .. import cli_custom_commands


class TestCustomClickCommandIterator(TestCase):
  """Tests for the CustomClickCommandIterator class."""

  def create_instance(self) -> cli_custom_commands.CustomClickCommandIterator:
    with patch(
        state.__name__ +
        ".user_configuration_file.UserConfigurationFile.load_yaml_file"
    ) as m_load:
      m_load.return_value = self.create_test_config()
      state.State().load()
      instance = cli_custom_commands.CustomClickCommandIterator()
    return instance

  def create_reversed_instance(self) -> List[click.Command]:
    instance = list(reversed(list(self.create_instance())))
    return instance

  def create_test_config(self) -> List[yaml_keys.TypeUserConfiguration]:
    return [
        {
            yaml_keys.PATH_METHOD: 'documentation_root',
            yaml_keys.COMMAND_NAME: 'test_command1',
            yaml_keys.COMMAND_DESCRIPTION: "The #1 test command",
            yaml_keys.COMMANDS: ["/bin/test_command1"],
            yaml_keys.SUCCESS: "Successful!",
            yaml_keys.FAILURE: "Failed!",
        }, {
            yaml_keys.PATH_METHOD: 'git_root',
            yaml_keys.COMMAND_NAME: 'test_command2',
            yaml_keys.CONTAINER_ONLY: True,
            yaml_keys.COMMAND_DESCRIPTION: "The #2 test command",
            yaml_keys.COMMANDS: ["/bin/test_command2"],
            yaml_keys.SUCCESS: "Successful!",
            yaml_keys.FAILURE: "Failed!",
        }
    ]

  def check_function_template(self, fn: click.Command, index: int) -> None:
    mock_config = self.create_test_config()
    self.assertIsInstance(fn, click.Command)

    self.assertEqual(
        fn.__doc__, mock_config[index][yaml_keys.COMMAND_DESCRIPTION]
    )
    self.assertEqual(fn.name, mock_config[index][yaml_keys.COMMAND_NAME])
    self.assertEqual(len(fn.params), 1)
    self.assertEqual(fn.params[0].human_readable_name, 'ARGS')
    self.assertFalse(fn.params[0].required,)
    self.assertIsInstance(
        fn.params[0].type,
        click.Path,
    )

  def check_invoke_template_function(
      self,
      index: int,
      overload: Tuple[str, ...],
  ) -> None:

    with ExitStack() as stack:
      m_select = stack.enter_context(
          patch(
              version_base.__name__ +
              ".UserConfigurationVersionBase.select_config_entry"
          )
      )
      m_customized = stack.enter_context(
          patch(cli_custom_commands.__name__ + ".customized.CustomizedCommand")
      )

      m_select.side_effect = [1, 0]

      click_commands = self.create_reversed_instance()
      mock_config = self.create_test_config()

      @click.group()
      def test() -> None:
        """Test command group."""

      test.add_command(click_commands[index])

      self.runner.invoke(
          test,
          f"{mock_config[index][yaml_keys.COMMAND_NAME]} {' '.join(overload)}"
      )

      self.assertEqual(m_customized.call_count, 1)

      m_customized.assert_called_once_with(
          command_configuration=index, overload=overload
      )
      m_customized.return_value.invoke.assert_called_once_with()

  def setUp(self) -> None:
    self.runner = CliRunner()
    state.State.clear()

  def test_initialization_configuration_commands(self) -> None:

    instance = self.create_instance()

    self.assertListEqual(
        instance.configuration_commands,
        [
            command[yaml_keys.COMMAND_NAME]
            for command in self.create_test_config()
        ],
    )

  def test_function_one(self) -> None:
    click_commands = self.create_reversed_instance()
    self.check_function_template(click_commands[0], 0)

  def test_function_two(self) -> None:
    click_commands = self.create_reversed_instance()
    self.check_function_template(click_commands[1], 1)

  def test_invoke_function_one(self) -> None:
    self.check_invoke_template_function(0, ())

  def test_invoke_function_two(self) -> None:
    self.check_invoke_template_function(1, ("overload1", "overload2"))
