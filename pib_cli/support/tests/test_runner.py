"""Tests for the CommandRunner class."""

from typing import Tuple
from unittest.mock import Mock, call, patch

from pib_cli import config
from pib_cli.config import yaml_keys
from pib_cli.support import state

from .. import runner
from .conftest import CommandRunnerCreatorType


class TestCommandRunner:
  """Tests for the CommandRunner class."""

  class TestInit:
    """Tests for initialization of the CommandRunner class."""

    def setup_method(self) -> None:
      state.State.clear()
      state.State().user_config = Mock()

    def test__initialize__without_overload__has_correct_properties(
        self,
        command_runner_creator: CommandRunnerCreatorType,
        mock_configuration: yaml_keys.TypeUserConfiguration,
    ) -> None:
      overload = ()

      instance = command_runner_creator(())

      assert instance.commands == mock_configuration[yaml_keys.COMMANDS]
      assert instance.exit_code == 127
      assert instance.overload == overload

    def test__initialize__with_overload__has_correct_properties(
        self,
        command_runner_creator: CommandRunnerCreatorType,
        mock_configuration: yaml_keys.TypeUserConfiguration,
    ) -> None:
      overload = ("one", "two", "three")

      instance = command_runner_creator(overload)

      assert instance.commands == mock_configuration[yaml_keys.COMMANDS]
      assert instance.exit_code == 127
      assert instance.overload == overload

  @patch(runner.__name__ + ".os")
  @patch(runner.__name__ + ".path_map.PathMap")
  class TestCommandRunnerExecute:
    """Tests for the execute method of the CommandRunner class."""

    mock_user_config: Mock

    def setup_method(self) -> None:
      state.State.clear()
      self.mock_user_config = Mock()
      state.State().user_config = self.mock_user_config

    def create_env_mocks(
        self,
        m_os: Mock,
        override_exists: bool,
    ) -> Tuple[Mock, Mock]:
      mock_setter = Mock()
      mock_deleter = Mock()

      m_os.environ.__setitem__ = mock_setter
      m_os.environ.__delitem__ = mock_deleter
      m_os.environ.__contains__.return_value = override_exists

      return mock_setter, mock_deleter

    def test__execute__invokes_chdir(
        self,
        m_path_map: Mock,
        _: Mock,
        command_runner_creator: CommandRunnerCreatorType,
        mock_configuration: yaml_keys.TypeUserConfiguration,
    ) -> None:
      instance = command_runner_creator(())

      instance.execute()

      assert mock_configuration[yaml_keys.PATH_METHOD] == "documentation_root"
      m_path_map.return_value.documentation_root.assert_called_once_with()

    def test__execute__with_overload__no_env__configures_env(
        self,
        _: Mock,
        m_os: Mock,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      mock_env_setter, _ = self.create_env_mocks(
          m_os,
          override_exists=False,
      )
      overload = ("one", "two", "three")
      instance = command_runner_creator(overload)

      instance.execute()

      assert mock_env_setter.mock_calls == [
          call(
              config.ENV_OVERRIDE_PROJECT_NAME,
              self.mock_user_config.get_project_name.return_value
          ),
          call(
              config.ENV_OVERRIDE_DOCUMENTATION_ROOT,
              self.mock_user_config.get_documentation_root.return_value,
          ),
          call(instance.overload_environment_variable, ' '.join(overload)),
      ]

    def test__execute__with_overload__with_env__configures_env(
        self,
        _: Mock,
        m_os: Mock,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      mock_env_setter, _ = self.create_env_mocks(
          m_os,
          override_exists=True,
      )
      overload = ("one", "two", "three")
      instance = command_runner_creator(overload)

      instance.execute()

      assert mock_env_setter.mock_calls == [
          call(instance.overload_environment_variable, ' '.join(overload)),
      ]

    def test__execute__with_overload__no_env__wipes_env(
        self,
        _: Mock,
        m_os: Mock,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      __, mock_env_deleter = self.create_env_mocks(
          m_os,
          override_exists=False,
      )
      overload = ("one", "two", "three")
      instance = command_runner_creator(overload)

      instance.execute()

      assert mock_env_deleter.mock_calls == [
          call(config.ENV_OVERRIDE_PROJECT_NAME,),
          call(config.ENV_OVERRIDE_DOCUMENTATION_ROOT,),
          call(instance.overload_environment_variable,),
      ]

    def test__execute__with_overload__with_env__wipes_env(
        self,
        _: Mock,
        m_os: Mock,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      __, mock_env_deleter = self.create_env_mocks(
          m_os,
          override_exists=True,
      )
      overload = ("one", "two", "three")
      instance = command_runner_creator(overload)

      instance.execute()

      assert mock_env_deleter.mock_calls == [
          call(instance.overload_environment_variable,),
      ]

    def test__execute__all_system_calls_successful__does_all_system_calls(
        self,
        _: Mock,
        m_os: Mock,
        mock_configuration: yaml_keys.TypeUserConfiguration,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      m_os.system.side_effect = (0, 0, 0)
      instance = command_runner_creator(())

      instance.execute()

      assert m_os.system.call_count == len(
          mock_configuration[yaml_keys.COMMANDS]
      )
      for custom_command in mock_configuration[yaml_keys.COMMANDS]:
        m_os.system.assert_any_call(custom_command)

    def test__execute__first_system_call_fails__does_1_system_call_only(
        self,
        _: Mock,
        m_os: Mock,
        mock_configuration: yaml_keys.TypeUserConfiguration,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      m_os.system.side_effect = (99 * 256,)
      instance = command_runner_creator(())

      instance.execute()

      assert m_os.system.mock_calls == [
          call(mock_configuration[yaml_keys.COMMANDS][0])
      ]

    def test__execute__second_system_call_fails__does_2_system_calls_only(
        self,
        _: Mock,
        m_os: Mock,
        mock_configuration: yaml_keys.TypeUserConfiguration,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      m_os.system.side_effect = (0, 99 * 256)
      instance = command_runner_creator(())

      instance.execute()

      assert m_os.system.mock_calls == [
          call(mock_configuration[yaml_keys.COMMANDS][0]),
          call(mock_configuration[yaml_keys.COMMANDS][1]),
      ]

    def test__execute__all_system_calls_successful__exit_code_is_0(
        self,
        _: Mock,
        m_os: Mock,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      m_os.system.side_effect = (0, 0, 0)
      instance = command_runner_creator(())

      instance.execute()

      assert instance.exit_code == 0

    def test__execute__first_system_call_fails__exit_code_is_99(
        self,
        _: Mock,
        m_os: Mock,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      m_os.system.side_effect = (99 * 256,)
      instance = command_runner_creator(())

      instance.execute()

      assert instance.exit_code == 99

    def test__execute__third_system_call_fails__exit_code_is_99(
        self,
        _: Mock,
        m_os: Mock,
        command_runner_creator: CommandRunnerCreatorType,
    ) -> None:
      m_os.system.side_effect = (0, 0, 99 * 256)
      instance = command_runner_creator(())

      instance.execute()

      assert instance.exit_code == 99
