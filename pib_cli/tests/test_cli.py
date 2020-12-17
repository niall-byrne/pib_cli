"""Test the CLI"""

from pib_cli.tests.fixtures import CommandTestHarness


class TestBuildDocs(CommandTestHarness):
  __test__ = True
  invocation_command = ['build-docs']
  expected_system_calls = ["make html"]
  success_message = "Documentation Built"
  failure_message = "Error Building Documentation"
  command_path_method = "project_docs"


class TestSecTest(CommandTestHarness):
  __test__ = True
  invocation_command = ['sectest']
  expected_system_calls = [
      'bandit -r "${PROJECT_NAME}" -c .bandit.rc --ini .bandit',
      'safety check',
  ]
  success_message = "Security Test Passes!"
  failure_message = "Security Test Failed!"
  command_path_method = "project_root"


class TestLint(CommandTestHarness):
  __test__ = True
  invocation_command = ['lint']
  expected_system_calls = [
      'isort -c "${PROJECT_NAME}"',
      ('pytest --pylint --pylint-rcfile=.pylint.rc '
       '--pylint-jobs=2 "${PROJECT_NAME}"'),
  ]
  success_message = "Lint Test Passes!"
  failure_message = "Lint Test Failed!"
  command_path_method = "project_root"
