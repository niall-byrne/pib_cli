"""Test the ContainerValidateCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

from pib_cli.support.container import exceptions

from .. import container_validate
from ..bases.fixtures import command_harness_exceptions


class TestContainerValidateCommand(
    command_harness_exceptions.CommandBaseExceptionsTestHarness
):
  """Test the ContainerValidateCommand class."""

  __test__ = True
  test_class = container_validate.ContainerValidateCommand
  instance: container_validate.ContainerValidateCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_click = stack.enter_context(
          patch(container_validate.__name__ + ".click")
      )
      m_container = stack.enter_context(
          patch(container_validate.__name__ + ".container.DevContainer")
      )
      m_container.return_value.container_valid_exception.side_effect = \
        self.side_effect
      m_sys = stack.enter_context(patch(container_validate.__name__ + ".sys"))
      self.instance.invoke()
    return m_click, m_container, m_sys

  def test_invoke(self) -> None:
    m_click, m_container, m_sys = self.invoke_command()
    m_container.assert_called_once_with()
    m_container.return_value.container_valid_exception.assert_called_once()
    m_click.echo.assert_called_once_with("This container is valid.")
    m_sys.assert_not_called()

  def test_invoke_exception(self) -> None:
    self.side_effect = exceptions.DevContainerException
    m_click, m_container, m_sys = self.invoke_command()
    m_container.assert_called_once_with()
    m_container.return_value.container_valid_exception.assert_called_once()
    m_click.echo.assert_called_once_with('No compatible PIB container found.')
    m_sys.exit.assert_called_once_with(
        m_container.return_value.incompatible_container_exit_code
    )
