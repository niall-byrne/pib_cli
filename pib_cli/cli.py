"""The Python In a Box Command Line Interface"""

import sys

import click
from .support.commands import Commands


def execute(command, overload=None):
  """Execute the specified command.

  command: A string representing the command
  overload: Additional parameters which will be inserted into the environment
  """

  command_manager = Commands()
  response = command_manager.invoke(command, overload)
  click.echo(response)
  sys.exit(command_manager.process_manager.exit_code)


@click.group()
def cli():
  """Development Environment CLI"""


@cli.command("build-docs")
def build_docs():
  """Build Documentation"""
  execute('build-docs')


@cli.command("build-wheel")
def build_wheel():
  """Build Distribution Wheel"""
  execute('build-wheel')


@cli.command(
    "coverage",
    context_settings=dict(
        ignore_unknown_options=True,
        help_option_names=[],
    ),
)
@click.argument('options', nargs=-1)
def coverage(options):
  """Run Unittests"""
  execute('coverage', overload=options)


@cli.command("fmt")
def formatter():
  """Run Code Formatters"""
  execute('fmt')


@cli.command("lint")
def linter_tests():
  """Run Linters"""
  execute('lint')


@cli.command("sectest")
def security_tests():
  """Run Security Tests"""
  execute('sectest')


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
  execute('test', overload=options)
