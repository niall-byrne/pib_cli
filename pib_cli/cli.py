"""The Python In a Box Command Line Interface"""

import sys

import click

from .support import internal_commands
from .support.external_commands import ExternalCommands


def execute_external_command(commands, overload=None):
  """Executes a batch of external commands.

  commands: A list of commands to be executed
  overload: Additional parameters which will be inserted into the environment
  """

  command_manager = ExternalCommands()

  for command in commands:
    response = command_manager.invoke(command, overload)
    click.echo(response)

    if command_manager.process_manager.exit_code != 0:
      break

  sys.exit(command_manager.process_manager.exit_code)


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
