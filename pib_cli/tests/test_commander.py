"""Test the Commander CLI"""

from pib_cli.tests.fixtures import CommandTestHarness


class TestBuildDocs(CommandTestHarness):
  __test__ = True
  invocation_command = ['build-docs']
  expected_system_call = "make html"
  success_message = "Documentation Built"
  failure_message = "Error Building Documentation"
  command_path_method = "project_docs"


class TestSecTest(CommandTestHarness):
  __test__ = True
  invocation_command = [
      'bandit -r "${PROJECT_NAME}" -c .bandit.rc --ini .bandit'
  ]
  expected_system_call = "make html"
  success_message = "Security Test Passes!"
  failure_message = "Security Test Failed!"
  command_path_method = "project_root"
