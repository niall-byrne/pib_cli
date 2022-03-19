"""Python-in-a-Box CLI entrypoint."""

from pib_cli.cli.interface import cli_interface


def main() -> None:
  """Entrypoint for pib_cli."""

  cli_interface()
