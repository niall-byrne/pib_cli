"""The Python In a Box Command Line Interface"""

import sys

import click
from .support.commands import Commands


def execute(command):
  command_manager = Commands()
  response = command_manager.invoke(command)
  click.echo(response)
  sys.exit(command_manager.process_manager.exit_code)


@click.group()
def cli():
  pass


@cli.command("build-docs")
def build_docs():
  execute('build-docs')


@cli.command("sectest")
def security_tests():
  execute('sectest')


@cli.command("lint")
def linter_tests():
  execute('lint')
