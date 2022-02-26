"""Test the ContainerVersion class."""

from typing import Optional, Tuple, Type
from unittest.mock import Mock, patch

from pib_cli.support.container import exceptions

from .. import container_version
from ..bases.fixtures import command_harness


class TestContainerSetup(command_harness.CommandBaseTestHarness):
  """Test the ContainerVersion class."""

  __test__ = True
  test_class = container_version.ContainerVersionCommand
  instance: container_version.ContainerVersionCommand

  def setUp(self) -> None:
    super().setUp()
    self.side_effect: Optional[Type[BaseException]] = None

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
      self.instance.invoke()
    return m_click, m_container

  def test_invoke(self) -> None:
    m_click, m_container = self.invoke_command()
    m_container.assert_called_once_with()
    m_container.return_value.get_container_version.assert_called_once()
    m_click.echo.assert_called_once_with(
        "Detected PIB container version: "
        f"{m_container.return_value.get_container_version.return_value}"
    )

  def test_invoke_outside_container(self) -> None:
    self.side_effect = exceptions.DevContainerException
    m_click, m_container = self.invoke_command()
    m_container.assert_called_once_with()
    m_container.return_value.get_container_version.assert_called_once()
    m_click.echo.assert_called_once_with('No PIB container found.')
