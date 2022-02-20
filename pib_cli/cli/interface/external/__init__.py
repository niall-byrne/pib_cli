"""Configuration managed CLI commands."""

import copy

import click
from pib_cli.support.external_commands import execute_external_command


@click.group()
def external():
  """Development Environment CLI."""


@external.command("build-docs")
def build_docs():
  """Build Documentation."""
  execute_external_command(['build-docs'])


@external.command("build-wheel")
def build_wheel():
  """Build Distribution Wheel."""
  execute_external_command(['build-wheel'])


@external.command(
    "coverage",
    context_settings=dict(
        ignore_unknown_options=True,
        help_option_names=[],
    ),
)
@click.argument('extra_options', nargs=-1)
def coverage(extra_options):
  """Run Code Coverage."""
  execute_external_command(['coverage'], overload=extra_options)


@external.command("fmt")
def formatter():
  """Run Code Formatters."""
  execute_external_command(['fmt'])


@external.command("leaks")
def leaks():
  """Run Credential Leak Scan."""
  execute_external_command(['leaks'])


@external.command("lint")
def linter_tests():
  """Run Code Linters."""
  execute_external_command(['lint'])


@external.command("reinstall-requirements")
def reinstall_requirements():
  """Reinstall Requirements."""
  execute_external_command(['reinstall-requirements'])


@external.command("sectest")
def security_tests():
  """Run Security Tests."""
  execute_external_command(['sectest'])


@external.command(
    "test",
    context_settings=dict(
        ignore_unknown_options=True,
        help_option_names=[],
    ),
)
@click.argument('extra_options', nargs=-1)
def unittests(extra_options):
  """Run Unittests."""
  execute_external_command(['test'], overload=extra_options)


@external.command("types")
def types():
  """Run Static Type Checker."""
  execute_external_command(['types'])


# Create a copy of the click group to allow Sphinx to reference the original
external_commands: click.Group = copy.deepcopy(external)
