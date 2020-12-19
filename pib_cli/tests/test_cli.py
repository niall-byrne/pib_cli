"""Test the CLI"""

from .fixtures import CommandTestHarness


class TestBuildDocs(CommandTestHarness):
  __test__ = True
  invocation_command = ['build-docs']
  external_commands = ['build-docs']


class TestBuildWheel(CommandTestHarness):
  __test__ = True
  invocation_command = ['build-wheel']
  external_commands = ['build-wheel']


class TestFormat(CommandTestHarness):
  __test__ = True
  invocation_command = ['fmt']
  external_commands = ['fmt']


class TestLint(CommandTestHarness):
  __test__ = True
  invocation_command = ['lint']
  external_commands = ['lint']


class TestSecTest(CommandTestHarness):
  __test__ = True
  invocation_command = ['sectest']
  external_commands = ['sectest']


class TestUnittests(CommandTestHarness):
  __test__ = True
  invocation_command = ['test']
  external_commands = ['test']
  overload = ()


class TestUnittestsOverload(CommandTestHarness):
  __test__ = True
  invocation_command = ['test']
  external_commands = ['test']
  overload = ('-s',)


class TestCoverage(CommandTestHarness):
  __test__ = True
  invocation_command = ['coverage']
  external_commands = ['coverage']
  overload = ()


class TestCoverageOverload(CommandTestHarness):
  __test__ = True
  invocation_command = ['coverage']
  external_commands = ['coverage']
  overload = ('/specific/file.py',)


class TestReinstallRequirements(CommandTestHarness):
  __test__ = True
  invocation_command = ['reinstall-requirements']
  external_commands = ['reinstall-requirements']


class TestSetupBash(CommandTestHarness):
  __test__ = True
  invocation_command = ['setup-bash']
  python_commands = ['setup-bash']


class TestSetup(CommandTestHarness):
  __test__ = True
  invocation_command = ['setup']
  python_commands = ['setup-bash']
  external_commands = ['reinstall-requirements']
