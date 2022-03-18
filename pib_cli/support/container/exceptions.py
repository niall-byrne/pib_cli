"""Development container exceptions."""

import sys
from typing import Any


class DevContainerException(BaseException):
  """Raised when the current environment is not the expected container type.

  :param exit_code: The exit code associated with this exception.
  """

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.exit_code = kwargs.pop('exit_code')
    super().__init__(*args, **kwargs)

  def exit(self) -> None:
    """Exit with the defined exit_code."""

    sys.exit(self.exit_code)
