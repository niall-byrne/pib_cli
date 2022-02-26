"""Test the VersionCommand class."""

from typing import Tuple
from unittest.mock import Mock, patch

import pkg_resources

from .. import version
from ..bases.fixtures import command_harness


class TestVersionCommand(command_harness.CommandBaseTestHarness):
  """Test the VersionCommand class."""

  __test__ = True
  test_class = version.VersionCommand
  instance: version.VersionCommand

  def invoke_command(self) -> Tuple[Mock, ...]:
    with self.mock_stack as stack:
      m_click = stack.enter_context(patch(version.__name__ + ".click"))
      self.instance.invoke()
    return (m_click,)

  def test_invoke(self) -> None:
    m_click = self.invoke_command()[0]
    m_click.echo.assert_called_once_with(
        f"pib_cli version: "
        f"{pkg_resources.get_distribution('pib_cli').version}",
    )
