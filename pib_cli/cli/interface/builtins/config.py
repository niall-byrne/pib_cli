"""Built in CLI configuration commands."""

from typing import Optional

import click
from pib_cli.cli.commands import (
    config_show,
    config_validate,
    config_version,
    config_where,
    handler,
)
from pib_cli.config.locale import _


@click.group(_("config"))
@click.option(
    "-c",
    "--config-file",
    help="A config file to use instead of the active one.",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    required=False,
)
@click.pass_context
def config(ctx: click.Context, config_file: Optional[str]) -> None:
  """PIB CLI configuration commands."""
  ctx.obj = {
      "config_file": config_file
  }


@config.command(_("show"))
@click.pass_context
def show_config_builtin(ctx: click.Context) -> None:
  """Display a CLI configuration file (defaults to the active file)."""

  handler(config_show.ConfigShowCommand, config_file=ctx.obj["config_file"])


@config.command(_("validate"))
@click.pass_context
def validate_config_builtin(ctx: click.Context) -> None:
  """Validate a CLI configuration file (defaults to the active file)."""

  handler(
      config_validate.ConfigValidateCommand, config_file=ctx.obj["config_file"]
  )


@config.command(_("version"))
@click.pass_context
def version_config_builtin(ctx: click.Context) -> None:
  """Find a CLI configuration file's version (defaults to the active file)."""

  handler(
      config_version.ConfigVersionCommand, config_file=ctx.obj["config_file"]
  )


@config.command(_("where"))
@click.pass_context
def where_config_builtin(ctx: click.Context) -> None:
  """Locate a CLI configuration file (defaults to the active file)."""

  handler(config_where.ConfigWhereCommand, config_file=ctx.obj["config_file"])


config_commands: click.Command = config
