"""Test the VersionCommand class."""

from unittest.mock import Mock, patch

import pkg_resources

from .. import version
from ..bases.fixtures import command_harness


class TestVersionCommand(command_harness.CommandBaseTestHarness):
  """Test the VersionCommand class."""

  __test__ = True
  test_class = version.VersionCommand

  @patch(version.__name__ + ".click")
  def test_invoke(self, m_module: Mock) -> None:
    self.instance.invoke()
    m_module.echo.assert_called_once_with(
        f"pib_cli version: "
        f"{pkg_resources.get_distribution('pib_cli').version}",
    )
