"""Tests for the CommandRunner class."""

from typing import Tuple
from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.config import yaml_keys

from .. import runner


class CommandRunnerTestHarness(TestCase):
  """Test harness for the CommandRunner class."""

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
    config = self.create_mock_config()
    return runner.CommandRunner(
        commands=config[yaml_keys.COMMANDS],
        overload=overload,
        path_map_method=config[yaml_keys.PATH_METHOD],
    )


class TestCommandRunnerInitialization(CommandRunnerTestHarness):
  """Tests for initialization of the CommandRunner class."""

  def test_initialize(self) -> None:
    config = self.create_mock_config()
    instance = self.create_instance(overload=())

    self.assertListEqual(
        instance.commands,
        config[yaml_keys.COMMANDS],
    )
    self.assertEqual(instance.exit_code, 127)
    self.assertEqual(instance.overload, ())

  def test_initialize_with_overload(self) -> None:
    overload = ("one", "two", "three")
    config = self.create_mock_config()
    instance = self.create_instance(overload=overload)

    self.assertListEqual(
        instance.commands,
        config[yaml_keys.COMMANDS],
    )
    self.assertEqual(instance.exit_code, 127)
    self.assertEqual(instance.overload, overload)


@patch(runner.__name__ + ".os")
@patch(runner.__name__ + ".path_map.PathMap")
class TestCommandRunnerExecution(CommandRunnerTestHarness):
  """Tests for the execution method of the CommandRunner class."""

  def test_invoke_chdir(self, m_path_map: Mock, _: Mock) -> None:
    instance = self.create_instance(overload=())
    instance.execute()

    m_path_map.return_value.documentation_root.assert_called_once_with()

  def test_invoke_overload(self, _: Mock, m_os: Mock) -> None:
    mock_setter = Mock()
    mock_delete = Mock()

    m_os.environ.__setitem__ = mock_setter
    m_os.environ.__delitem__ = mock_delete
    m_os.environ.__contains__.return_value = False

    overload = ("one", "two", "three")
    instance = self.create_instance(overload=overload)
    instance.execute()

    mock_setter.assert_called_once_with(
        instance.overload_environment_variable, ' '.join(overload)
    )
    mock_delete.assert_not_called()

  def test_invoke_does_not_clean_overload(self, _: Mock, m_os: Mock) -> None:
    mock_setter = Mock()
    mock_delete = Mock()

    m_os.environ.__setitem__ = mock_setter
    m_os.environ.__delitem__ = mock_delete
    m_os.environ.__contains__.return_value = True

    overload = ("one", "two", "three")
    instance = self.create_instance(overload=overload)
    instance.execute()

    mock_setter.assert_called_once_with(
        instance.overload_environment_variable, ' '.join(overload)
    )
    mock_delete.assert_called_once_with(instance.overload_environment_variable,)

  def test_invoke_cleans_overload(self, _: Mock, m_os: Mock) -> None:
    mock_setter = Mock()
    mock_delete = Mock()

    m_os.environ.__setitem__ = mock_setter
    m_os.environ.__delitem__ = mock_delete
    m_os.environ.__contains__.return_value = True

    overload = ("one", "two", "three")
    instance = self.create_instance(overload=overload)
    instance.execute()

    mock_setter.assert_called_once_with(
        instance.overload_environment_variable, ' '.join(overload)
    )
    mock_delete.assert_called_once_with(instance.overload_environment_variable,)

  def test_invoke_makes_all_system_calls(self, _: Mock, m_os: Mock) -> None:
    m_os.system.side_effect = (0, 0, 0)
    config = self.create_mock_config()

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(m_os.system.call_count, len(config[yaml_keys.COMMANDS]))

    for custom_command in config[yaml_keys.COMMANDS]:
      m_os.system.assert_any_call(custom_command)

  def test_invoke_stops_after_first_system_call(
      self, _: Mock, m_os: Mock
  ) -> None:
    m_os.system.side_effect = (99 * 256,)
    config = self.create_mock_config()

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(m_os.system.call_count, 1)

    m_os.system.assert_called_once_with(config[yaml_keys.COMMANDS][0])

  def test_invoke_stops_after_second_system_call(
      self, _: Mock, m_os: Mock
  ) -> None:
    m_os.system.side_effect = (0, 99 * 256)
    config = self.create_mock_config()

    instance = self.create_instance(overload=())
    instance.execute()

    self.assertEqual(m_os.system.call_count, 2)

    for custom_command in config[yaml_keys.COMMANDS][0:1]:
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
