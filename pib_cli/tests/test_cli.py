"""Test the CLI Invocation."""

from .fixtures import CommandTestHarness


class TestBuildDocs(CommandTestHarness):
  """Test the build-docs command."""

  __test__ = True
  invocation_command = ['build-docs']
  external_commands = ['build-docs']


class TestBuildWheel(CommandTestHarness):
  """Test the build-wheel command."""

  __test__ = True
  invocation_command = ['build-wheel']
  external_commands = ['build-wheel']


class TestFormat(CommandTestHarness):
  """Test the fmt command."""

  __test__ = True
  invocation_command = ['fmt']
  external_commands = ['fmt']


class TestLeaks(CommandTestHarness):
  """Test the leaks command."""

  __test__ = True
  invocation_command = ['leaks']
  external_commands = ['leaks']


class TestLint(CommandTestHarness):
  """Test the lint command."""

  __test__ = True
  invocation_command = ['lint']
  external_commands = ['lint']


class TestSecTest(CommandTestHarness):
  """Test the sectest command."""

  __test__ = True
  invocation_command = ['sectest']
  external_commands = ['sectest']


class TestUnittests(CommandTestHarness):
  """Test the test command."""

  __test__ = True
  invocation_command = ['test']
  external_commands = ['test']
  overload = ()


class TestUnittestsOverload(CommandTestHarness):
  """Test the test command with overloads."""

  __test__ = True
  invocation_command = ['test']
  external_commands = ['test']
  overload = ('-s',)


class TestCoverage(CommandTestHarness):
  """Test the coverage command."""

  __test__ = True
  invocation_command = ['coverage']
  external_commands = ['coverage']
  overload = ()


class TestCoverageOverload(CommandTestHarness):
  """Test the coverage command with overloads."""

  __test__ = True
  invocation_command = ['coverage']
  external_commands = ['coverage']
  overload = ('/specific/file.py',)


class TestReinstallRequirements(CommandTestHarness):
  """Test the reinstall-requirements command."""

  __test__ = True
  invocation_command = ['reinstall-requirements']
  external_commands = ['reinstall-requirements']


class TestTypes(CommandTestHarness):
  """Test the types command."""

  __test__ = True
  invocation_command = ['types']
  external_commands = ['types']
