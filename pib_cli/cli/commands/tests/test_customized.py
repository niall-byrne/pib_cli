"""Test the CustomizedCommand class."""

from typing import Tuple, Type
from unittest.mock import Mock, patch

from pib_cli.support.container import exceptions

from .. import customized
from ..bases.fixtures import command_harness


class TestCustomizedCommand(command_harness.CommandBaseTestHarness):
  """Test the CustomizedCommand class."""

  __test__ = True
  instance: customized.CustomizedCommand
  test_class: Type[customized.CustomizedCommand]

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = customized.CustomizedCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_runner = stack.enter_context(
          patch(customized.__name__ + ".runner.CommandRunner")
      )
      m_exit = stack.enter_context(patch(customized.__name__ + ".sys.exit"))
      m_click = stack.enter_context(patch(customized.__name__ + ".click"))
      self.instance.invoke()
    return m_runner, m_exit, m_click

  def setUp(self) -> None:
    self.mock_command_configuration = Mock()
    self.mock_overload = (
        "one",
        "two",
    )
    self.instance = self.test_class(
        command_configuration=self.mock_command_configuration,
        overload=self.mock_overload,
    )

  def test_initialize(self) -> None:
    self.assertEqual(
        self.instance.command_configuration, self.mock_command_configuration
    )
    self.assertEqual(self.instance.container_only_error_exit_code, 127)
    self.assertEqual(self.instance.overload, self.mock_overload)

  def test_invoke(self) -> None:
    m_runner, _, m_click = self.invoke_command()

    self.mock_command_configuration.get_config_response.assert_called_once_with(
        m_runner.return_value.exit_code
    )
    m_click.echo.assert_called_once_with(
        self.mock_command_configuration.get_config_response.return_value
    )

  def test_invoke_executes_runner(self) -> None:
    m_runner, _, __ = self.invoke_command()

    m_runner.assert_called_once_with(
        commands=self.mock_command_configuration.get_config_commands.
        return_value,
        path_map_method=self.mock_command_configuration.get_config_path_method.
        return_value,
        overload=self.mock_overload
    )
    m_runner.return_value.execute.assert_called_once_with()

  def test_invoke_exits_correctly(self) -> None:
    m_runner, m_exit, _ = self.invoke_command()
    m_exit.assert_called_once_with(m_runner.return_value.exit_code)

  def test_invoke_container_only_cannot_execute(self) -> None:
    error_message = "test_message"

    with patch.object(
        self.instance.command_configuration, "is_executable_exception"
    ) as m_executable:
      m_executable.side_effect = exceptions.DevContainerException(error_message)
      _, m_exit, m_click = self.invoke_command()

    m_click.echo.assert_called_once_with(f"ERROR: {error_message}")
    m_exit.assert_called_once_with(self.instance.container_only_error_exit_code)
