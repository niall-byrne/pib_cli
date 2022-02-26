"""Test the ContainerSetupCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

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
      m_installer = stack.enter_context(
          patch(container_setup.__name__ + ".installer.DevContainerInstaller")
      )
      self.instance.invoke()
    return m_click, m_installer

  def test_invoke(self) -> None:
    m_click, m_installer = self.invoke_command()
    m_installer.assert_called_once_with()
    m_installer.return_value.container_valid_exception.assert_called_once()
    m_installer.return_value.setup.assert_called_once_with(m_click.echo)
