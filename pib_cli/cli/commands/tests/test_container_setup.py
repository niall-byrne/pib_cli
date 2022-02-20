"""Test the ContainerSetup class."""

from unittest.mock import Mock, patch

from .. import container_setup
from ..bases.fixtures import command_harness


class TestContainerSetup(command_harness.CommandBaseTestHarness):
  """Test the ContainerSetup class."""

  __test__ = True
  test_class = container_setup.ContainerSetupCommand

  @patch(container_setup.__name__ + ".click")
  def test_invoke(self, m_module: Mock) -> None:
    with patch(
        container_setup.__name__ + ".installer.DevContainerInstaller"
    ) as m_installer:
      self.instance.invoke()

    m_installer.assert_called_once_with()
    m_installer.return_value.container_valid_exception.assert_called_once()
    m_installer.return_value.setup.assert_called_once_with(m_module.echo)
