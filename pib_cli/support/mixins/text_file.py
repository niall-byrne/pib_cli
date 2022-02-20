"""TextFile mixin classes."""

from pathlib import Path
from typing import Union


class TextFileReader:
  """TextFileReader mixin class."""

  encoding = "utf-8"

  def load_text_file(self, text_file_location: Union[Path, str]) -> str:
    """Load a text file from the file system and return it as a string.

    :param text_file_location: The path to the source file.
    :returns: The loaded string object.
    """
    with open(text_file_location, encoding=self.encoding) as file_handle:
      data = file_handle.read()
    return data
