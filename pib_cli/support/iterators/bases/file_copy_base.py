"""FileCopyIteratorBase class."""

import abc
import glob
from typing import NamedTuple

SourceDestinationPair = NamedTuple(
    "SourceDestinationPair",
    [
        ("source", str),
        ("destination", str),
    ],
)


class FileCopyIteratorBase(abc.ABC):
  """A base iterator for generating pairs of source, destination files.

  Creates a sequence of
  :class:`.SourceDestinationPair`.
  """

  glob_pattern: str

  def __init__(self) -> None:
    self.files = glob.glob(self.glob_pattern)

  @abc.abstractmethod
  def hook_create_destination(self, current_source: str) -> str:
    """Override to construct the file's destination path.

    :param current_source: The path to the source file.
    """

  def __next__(self) -> SourceDestinationPair:
    while self.files:
      current_source = self.files.pop()
      current_destination = self.hook_create_destination(current_source)
      return_value = SourceDestinationPair(current_source, current_destination)
      return return_value
    raise StopIteration

  def __iter__(self) -> "FileCopyIteratorBase":
    return self
