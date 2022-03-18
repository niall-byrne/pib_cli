"""Test the ContainerVersionCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

from pib_cli.support.container import exceptions

from .. import container_version
from ..bases.fixtures import command_harness_exceptions


class TestContainerVersionCommand(
    command_harness_exceptions.CommandBaseExceptionsTestHarness
):
  """Test the ContainerVersionCommand class."""

  __test__ = True
  test_class = container_version.ContainerVersionCommand
  instance: container_version.ContainerVersionCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_click = stack.enter_context(
          patch(container_version.__name__ + ".click")
      )
      m_container = stack.enter_context(
          patch(container_version.__name__ + ".container.DevContainer")
      )
      m_container.return_value.get_container_version.side_effect = \
        self.side_effect
      m_sys = stack.enter_context(patch(container_version.__name__ + ".sys"))
      self.instance.invoke()
    return m_click, m_container, m_sys

  def test_invoke(self) -> None:
    m_click, m_container, m_sys = self.invoke_command()
    m_container.assert_called_once_with()
    m_container.return_value.get_container_version.assert_called_once()
    m_click.echo.assert_called_once_with(
        "Container version: "
        f"{m_container.return_value.get_container_version.return_value}"
    )
    m_sys.assert_not_called()

  def test_invoke_exception(self) -> None:
    self.side_effect = exceptions.DevContainerException
    m_click, m_container, m_sys = self.invoke_command()
    m_container.assert_called_once_with()
    m_container.return_value.get_container_version.assert_called_once()
    m_click.echo.assert_called_once_with('No PIB container found.')
    m_sys.exit.assert_called_once_with(
        m_container.return_value.incompatible_container_exit_code
    )
