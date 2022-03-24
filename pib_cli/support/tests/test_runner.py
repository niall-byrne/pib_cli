"""Tests for the CommandRunner class."""

from typing import Tuple
from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli import config
from pib_cli.config import yaml_keys
from pib_cli.support import state

from .. import runner


class CommandRunnerTestHarness(TestCase):
  """Test harness for the CommandRunner class."""

  mock_user_config: Mock

  def setUp(self) -> None:
    state.State.clear()
    self.mock_user_config = Mock()
    state.State().user_config = self.mock_user_config

  def create_mock_config(self) -> yaml_keys.TypeUserConfiguration:
    return {
        yaml_keys.PATH_METHOD: 'documentation_root',
        yaml_keys.COMMAND_NAME: 'test_command',
        yaml_keys.COMMAND_DESCRIPTION: "The test command",
        yaml_keys.COMMANDS:
            [
                "/bin/test_command_step_1",
                "/bin/test_command_step_2",
                "/bin/test_command_step_3",
            ],
        yaml_keys.SUCCESS: "Successful!",
        yaml_keys.FAILURE: "Failed!",
    }

  def create_instance(self, overload: Tuple[str, ...]) -> runner.CommandRunner:
    cli_config = self.create_mock_config()
    return runner.CommandRunner(
        commands=cli_config[yaml_keys.COMMANDS],
        overload=overload,
        path_map_method=cli_config[yaml_keys.PATH_METHOD],
    )


class TestCommandRunnerInitialization(CommandRunnerTestHarness):
  """Tests for initialization of the CommandRunner class."""

  def test_initialize(self) -> None:
    cli_config = self.create_mock_config()
    instance = self.create_instance(overload=())

    self.assertListEqual(
        instance.commands,
        cli_config[yaml_keys.COMMANDS],
    )
    self.assertEqual(instance.exit_code, 127)
    self.assertEqual(instance.overload, ())

  def test_initialize_with_overload(self) -> None:
    overload = ("one", "two", "three")
    cli_config = self.create_mock_config()
    instance = self.create_instance(overload=overload)

    self.assertListEqual(
        instance.commands,
        cli_config[yaml_keys.COMMANDS],
    )
    self.assertEqual(instance.exit_code, 127)
    self.assertEqual(instance.overload, overload)


@patch(runner.__name__ + ".os")
@patch(runner.__name__ + ".path_map.PathMap")
class TestCommandRunnerExecution(CommandRunnerTestHarness):
  """Tests for the execution method of the CommandRunner class."""

  def create_env_mocks(self, m_os: Mock, exists: bool) -> Tuple[Mock, Mock]:
    mock_setter = Mock()
    mock_deleter = Mock()

    m_os.environ.__setitem__ = mock_setter
    m_os.environ.__delitem__ = mock_deleter
    m_os.environ.__contains__.return_value = exists

    return mock_setter, mock_deleter

  def test_invoke_chdir(self, m_path_map: Mock, _: Mock) -> None:
    instance = self.create_instance(overload=())
    instance.execute()

    m_path_map.return_value.documentation_root.assert_called_once_with()

  def test_invoke_overload_no_env_vars(self, _: Mock, m_os: Mock) -> None:
    mock_setter, mock_deleter = self.create_env_mocks(m_os, exists=False)

    overload = ("one", "two", "three")
    instance = self.create_instance(overload=overload)
    instance.execute()

    mock_setter.assert_any_call(
        instance.overload_environment_variable, ' '.join(overload)
    )
    mock_setter.assert_any_call(
        config.ENV_OVERRIDE_PROJECT_NAME,
        self.mock_user_config.get_project_name.return_value,
    )
    mock_setter.assert_any_call(
        config.ENV_OVERRIDE_DOCUMENTATION_ROOT,
        self.mock_user_config.get_documentation_root.return_value,
    )
    self.assertEqual(mock_setter.call_count, 3)

    mock_deleter.assert_any_call(config.ENV_OVERRIDE_PROJECT_NAME,)
    mock_deleter.assert_any_call(config.ENV_OVERRIDE_DOCUMENTATION_ROOT,)
    mock_deleter.assert_any_call(instance.overload_environment_variable,)
    self.assertEqual(mock_deleter.call_count, 3)

  def test_invoke_overload_env_vars_exist(self, _: Mock, m_os: Mock) -> None:
    mock_setter, mock_deleter = self.create_env_mocks(m_os, exists=True)

    overload = ("one", "two", "three")
    instance = self.create_instance(overload=overload)
    instance.execute()

    mock_setter.assert_called_once_with(
        instance.overload_environment_variable, ' '.join(overload)
    )
    mock_deleter.assert_called_once_with(
        instance.overload_environment_variable,
    )

  def test_invoke_makes_all_system_calls(self, _: Mock, m_os: Mock) -> None:
    m_os.system.side_effect = (0, 0, 0)
    cli_config = self.create_mock_config()

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(
        m_os.system.call_count, len(cli_config[yaml_keys.COMMANDS])
    )

    for custom_command in cli_config[yaml_keys.COMMANDS]:
      m_os.system.assert_any_call(custom_command)

  def test_invoke_stops_after_first_system_call(
      self, _: Mock, m_os: Mock
  ) -> None:
    m_os.system.side_effect = (99 * 256,)
    cli_config = self.create_mock_config()

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(m_os.system.call_count, 1)

    m_os.system.assert_called_once_with(cli_config[yaml_keys.COMMANDS][0])

  def test_invoke_stops_after_second_system_call(
      self, _: Mock, m_os: Mock
  ) -> None:
    m_os.system.side_effect = (0, 99 * 256)
    cli_config = self.create_mock_config()

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(m_os.system.call_count, 2)

    for custom_command in cli_config[yaml_keys.COMMANDS][0:1]:
      m_os.system.assert_any_call(custom_command)

  def test_exit_code_zero_all(self, _: Mock, m_os: Mock) -> None:
    m_os.system.side_effect = (0, 0, 0)

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(instance.exit_code, 0)

  def test_exit_code_non_zero_first(self, _: Mock, m_os: Mock) -> None:
    m_os.system.side_effect = (99 * 256,)

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(instance.exit_code, 99)

  def test_exit_code_non_zero_last(self, _: Mock, m_os: Mock) -> None:
    m_os.system.side_effect = (0, 0, 99 * 256)

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(instance.exit_code, 99)
