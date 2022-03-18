"""Test the ContainerSetupCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

from pib_cli.support.container import exceptions

from .. import container_setup
from ..bases.fixtures import command_harness


class TestContainerSetupCommand(command_harness.CommandBaseTestHarness):
  """Test the ContainerSetupCommand class."""

  __test__ = True
  test_class = container_setup.ContainerSetupCommand
  instance: container_setup.ContainerSetupCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_click = stack.enter_context(patch(container_setup.__name__ + ".click"))
      m_exit = stack.enter_context(
          patch(
              container_setup.__name__ +
              ".exceptions.DevContainerException.exit"
          )
      )
      m_installer = stack.enter_context(
          patch(container_setup.__name__ + ".installer.DevContainerInstaller")
      )
      if self.test_exception:
        m_installer.side_effect = self.test_exception
      self.instance.invoke()
    return m_click, m_exit, m_installer

  def test_invoke(self) -> None:
    m_click, _, m_installer = self.invoke_command()
    m_installer.assert_called_once_with()
    m_installer.return_value.container_valid_exception.assert_called_once()
    m_installer.return_value.setup.assert_called_once_with(m_click.echo)

  def test_invoke_container_only_cannot_execute(self) -> None:
    error_message = "test_message"
    exit_code = 1
    self.test_exception = exceptions.DevContainerException(
        error_message, exit_code=exit_code
    )

    m_click, m_exit, _ = self.invoke_command()
    m_click.echo.assert_called_once_with(f"ERROR: {error_message}")
    m_exit.assert_called_once_with()
