"""CommandSelectorBase class."""

import abc
from typing import List, Union

from pib_cli.config import yaml_keys
from pib_cli.support import container


class CommandSelectorBase(abc.ABC):
  """A parsed end-user configuration entry, ready to use."""

  def __init__(
      self,
      user_configuration: Union[yaml_keys.TypeLegacyUserConfiguration,
                                yaml_keys.TypeUserConfiguration],
  ) -> None:
    self.container = container.DevContainer()
    self.user_configuration = user_configuration
    self.user_configuration[yaml_keys.COMMANDS] = \
      self._str_to_list(
        self.user_configuration[yaml_keys.COMMANDS]
      )

  def _str_to_list(self, command: Union[str, List[str]]) -> List[str]:
    if isinstance(command, str):
      return [command]
    return command

  @abc.abstractmethod
  def get_config_path_method(self) -> str:
    """Return the path method associated with the selected yaml config."""

  def get_config_commands(self) -> List[str]:
    """Return the commands section of the selected yaml config.

    :returns: A list of commands from the selected yaml config.
    """
    return self.user_configuration[yaml_keys.COMMANDS]

  def get_config_response(self, exit_code: int) -> str:
    """Return the response message content based on the command exit code.

    :param exit_code: The exit code returned by a process.
    :returns: The response message for the given exit_code.
    """
    if exit_code == 0:
      return self.user_configuration[yaml_keys.SUCCESS]
    return self.user_configuration[yaml_keys.FAILURE]

  def is_executable_exception(self) -> None:
    """Determine if the currently selected command can be executed or not.

    :raises: :class:`.DevContainerException`
    """
    container_only_flag = self.user_configuration.get(
        yaml_keys.CONTAINER_ONLY,
        False,
    )

    if container_only_flag:
      self.container.container_valid_exception()
