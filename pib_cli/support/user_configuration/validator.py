"""UserConfigurationValidator class."""

from pathlib import Path
from typing import Any

from jsonschema import validate
from pib_cli import config, config_filename
from pib_cli.support.mixins import json_file


class UserConfigurationValidator(json_file.JSONFileReader):
  """Validator for end-user configuration."""

  schema_file = Path(config.__file__).parent / "schema.json"
  config_filename = config_filename

  def __init__(self) -> None:
    self.schema = self.load_json_file(self.schema_file)

  def validate(self, loaded_user_configuration: Any) -> None:
    """Perform validation on the end-user configuration against the schema.

    :param loaded_user_configuration: A Python object containing user config.
    :raises: :class:`jsonschema.exceptions.ValidationError`
    """

    validate(loaded_user_configuration, self.schema)
