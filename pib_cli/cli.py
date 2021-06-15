"""The Python In a Box Command Line Interface."""

import click

from .support.external_commands import execute_external_command
from .support.internal_commands import execute_internal_command


@click.group()
def cli():
  """Development Environment CLI"""


@cli.command("build-docs")
def build_docs():
  """Build Documentation"""
  execute_external_command(['build-docs'])


@cli.command("build-wheel")
def build_wheel():
  """Build Distribution Wheel"""
  execute_external_command(['build-wheel'])


@cli.command("config-location")
def config_location():
  """Show location of the current configuration file"""
  execute_internal_command(['config_location'])


@cli.command("config-show")
def config_show():
  """Show current configuration file"""
  execute_internal_command(['config_show'])


@cli.command(
    "coverage",
    context_settings=dict(
        ignore_unknown_options=True,
        help_option_names=[],
    ),
)
@click.argument('extra_options', nargs=-1)
def coverage(extra_options):
  """Run Code Coverage"""
  execute_external_command(['coverage'], overload=extra_options)


@cli.command("fmt")
def formatter():
  """Run Code Formatters"""
  execute_external_command(['fmt'])


@cli.command("leaks")
def leaks():
  """Run Credential Leak Scan"""
  execute_external_command(['leaks'])


@cli.command("lint")
def linter_tests():
  """Run Code Linters"""
  execute_external_command(['lint'])


@cli.command("reinstall-requirements")
def reinstall_requirements():
  """Reinstall Requirements"""
  execute_external_command(['reinstall-requirements'])


@cli.command("sectest")
def security_tests():
  """Run Security Tests"""
  execute_external_command(['sectest'])


@cli.command("setup-bash")
def setup_bash():
  """Setup Bash Environment"""
  execute_internal_command(["setup_bash"])


@cli.command("setup")
@click.pass_context
def setup_environment(ctx):
  """Setup Environment"""
  ctx.invoke(setup_bash)
  execute_external_command(['reinstall-requirements'])


@cli.command(
    "test",
    context_settings=dict(
        ignore_unknown_options=True,
        help_option_names=[],
    ),
)
@click.argument('extra_options', nargs=-1)
def unittests(extra_options):
  """Run Unittests"""
  execute_external_command(['test'], overload=extra_options)


@cli.command("types")
def types():
  """Run Static Type Checker"""
  execute_external_command(['types'])


@cli.command("version")
def version():
  """Report the CLI Version"""
  execute_internal_command(["version"])
