"""UserConfigurationValidator class."""

from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict

from jsonschema import RefResolver, exceptions, validate
from pib_cli import config
from pib_cli.support import state
from pib_cli.support.mixins import json_file


class UserConfigurationValidator(json_file.JSONFileReader):
  """Validator for end-user configuration."""

  active_schemas: Dict[str, str] = OrderedDict(
      {
          "2.1.0": "cli_base_schema_v2.1.0.json",
          "2.0.0": "cli_cmd_schema_v0.1.0.json",
      }
  )
  _schema_folder = Path(config.__file__).parent / "schemas"

  def __init__(self) -> None:
    self.config_filename = state.State().user_config_file.get_config_file_name()
    self.schemas: Dict[str, Any] = {}
    for schema_version, schema_path in self.active_schemas.items():
      self.schemas[schema_version] = self.load_json_file(
          self._schema_folder / schema_path
      )

  def validate(self, loaded_user_configuration: Any) -> str:
    """Perform validation on the end-user configuration against the schema.

    :param loaded_user_configuration: A Python object containing user config.
    :returns: The first configuration schema version that passes validation.
    :raises: :class:`jsonschema.exceptions.ValidationError`
    """

    validation_exception = exceptions.ValidationError("No schema found!")

    for version, schema in self.schemas.items():
      try:
        resolver = RefResolver("file://" + str(self._schema_folder), None)
        validate(loaded_user_configuration, schema, resolver=resolver)
        return version
      except exceptions.ValidationError as last_exception:
        validation_exception = last_exception

    raise validation_exception
