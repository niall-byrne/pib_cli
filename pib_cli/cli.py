"""The Python In a Box Command Line Interface"""

import click

from .support import internal_commands
from .support.external_commands import execute_external_command


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


@cli.command(
    "coverage",
    context_settings=dict(
        ignore_unknown_options=True,
        help_option_names=[],
    ),
)
@click.argument('options', nargs=-1)
def coverage(options):
  """Run Code Coverage"""
  execute_external_command(['coverage'], overload=options)


@cli.command("fmt")
def formatter():
  """Run Code Formatters"""
  execute_external_command(['fmt'])


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
  result = internal_commands.setup_bash()
  click.echo(result)


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
@click.argument('options', nargs=-1)
def unittests(options):
  """Run Unittests"""
  execute_external_command(['test'], overload=options)
