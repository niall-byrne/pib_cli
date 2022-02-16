"""YAMLFile mixin classes."""

from pathlib import Path
from typing import Any, Union

import yaml


class YAMLFileReader:
  """YAMLFileReader mixin class."""

  encoding = "utf-8"

  def load_yaml_file(self, yaml_file_location: Union[Path, str]) -> Any:
    """Load a YAML file from the filesystem and return it as a Python object.

    :param yaml_file_location: The path to the source file.
    :returns: The loaded YAML as a Python object.
    """

    with open(yaml_file_location, encoding=self.encoding) as fhandle:
      yaml_file_content = yaml.safe_load(fhandle)
    return yaml_file_content
