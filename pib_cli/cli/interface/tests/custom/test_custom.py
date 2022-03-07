"""Test commands for the default customized CLI interface."""

from pib_cli.cli.interface.tests.fixtures import custom_cli_harness


class TestBuildWheel(custom_cli_harness.CustomCLIInterfaceTestHarness):
  """Test the default custom 'build-wheel' CLI command interface."""

  __test__ = True
  cli_command_string = "build-wheel"


class TestCoverage(custom_cli_harness.CustomCLIInterfaceTestHarness):
  """Test the default custom 'coverage' CLI command interface."""

  __test__ = True
  cli_command_string = "coverage"


class TestFormat(custom_cli_harness.CustomCLIInterfaceTestHarness):
  """Test the default custom 'fmt' CLI command interface."""

  __test__ = True
  cli_command_string = "fmt"


class TestLeaks(custom_cli_harness.CustomCLIInterfaceTestHarness):
  """Test the default custom 'leaks' CLI command interface."""

  __test__ = True
  cli_command_string = "leaks"


class TestLint(custom_cli_harness.CustomCLIInterfaceTestHarness):
  """Test the default custom 'lint' CLI command interface."""

  __test__ = True
  cli_command_string = "lint"


class TestReinstallRequirements(
    custom_cli_harness.CustomCLIInterfaceTestHarness
):
  """Test the default custom 'reinstall-requirements' CLI command interface."""

  __test__ = True
  cli_command_string = "reinstall-requirements"


class TestSecurityTest(custom_cli_harness.CustomCLIInterfaceTestHarness):
  """Test the default custom 'sectest' CLI command interface."""

  __test__ = True
  cli_command_string = "sectest"


class TestUnittests(custom_cli_harness.CustomCLIInterfaceTestHarness):
  """Test the default custom 'test' CLI command interface."""

  __test__ = True
  cli_command_string = "test"
