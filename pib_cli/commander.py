"""The Python In a Box Command Line Interface"""

import sys

import click
from .support.cli_utilities import Utilities


@click.group()
@click.pass_context
def cli(ctx):
  ctx.ensure_object(dict)
  ctx.obj['util'] = Utilities()


@cli.command("build-docs")
@click.pass_context
def build_docs(ctx):
  process_manager = ctx.obj['util'].process_manager
  path_manager = ctx.obj['util'].path_manager

  path_manager.project_docs()
  process_manager.spawn(["make html"])

  if process_manager.exit_code != 0:
    click.echo('Error Building Documentation')
    sys.exit(process_manager.exit_code)
  click.echo('Documentation Built')


@cli.command("sectest")
@click.pass_context
def security_tests(ctx):
  process_manager = ctx.obj['util'].process_manager
  path_manager = ctx.obj['util'].path_manager

  path_manager.project_root()
  process_manager.spawn([
      'bandit -r "${PROJECT_NAME}" -c .bandit.rc --ini .bandit',
      'safety check',
  ])

  if process_manager.exit_code != 0:
    click.echo('Security Test Failed!')
    sys.exit(process_manager.exit_code)
  click.echo('Security Test Passes!')


@cli.command("lint")
@click.pass_context
def linter_tests(ctx):
  process_manager = ctx.obj['util'].process_manager
  path_manager = ctx.obj['util'].path_manager

  path_manager.project_root()
  process_manager.spawn([
      'isort -c "${PROJECT_NAME}"',
      ('pytest --pylint --pylint-rcfile=.pylint.rc '
       '--pylint-jobs=2 "${PROJECT_NAME}"'),
  ])

  if process_manager.exit_code != 0:
    click.echo('Lint Test Failed!')
    sys.exit(process_manager.exit_code)
  click.echo("Lint Test Passes!")
