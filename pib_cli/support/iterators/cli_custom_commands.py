"""CustomClickCommandIterator class."""

from typing import Callable, Tuple

import click
from pib_cli.cli.commands import customized
from pib_cli.config import yaml_keys
from pib_cli.support import user_configuration


class CustomClickCommandIterator:
  """An iterator that produces Click commands from end-user configuration.

  Creates a sequence of :class:`click.Command`.
  """

  def __init__(self) -> None:
    self.user_configuration = user_configuration.UserConfiguration()
    self.user_configuration.validate()
    self.configuration_commands = list(
        self.user_configuration.configuration_command_index.keys()
    )

  def __next__(self) -> click.Command:
    if self.configuration_commands:
      command_name = self.configuration_commands.pop()
      template_function = self._create_template_function(command_name)
      return click.command(
          command_name,
          context_settings=dict(ignore_unknown_options=True),
      )(template_function)

    raise StopIteration

  def _create_template_function(
      self,
      command_name: str,
  ) -> Callable[[Tuple[str, ...]], None]:

    command_selected_entry = self.user_configuration.select_config_entry(
        command_name
    )
    command_configuration = self.user_configuration.configuration_command_index[
        command_name]

    @click.argument('args', type=click.Path(file_okay=True), nargs=-1)
    def template_function(args: Tuple[str, ...]) -> None:
      configuration_based_command = customized.CustomizedCommand(
          command_configuration=command_selected_entry,
          overload=args,
      )
      configuration_based_command.invoke()

    template_function.__name__ = command_name
    template_function.__doc__ = command_configuration[
        yaml_keys.COMMAND_DESCRIPTION]

    return template_function

  def __iter__(self) -> "CustomClickCommandIterator":
    return self
