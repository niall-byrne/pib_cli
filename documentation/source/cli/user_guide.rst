PIB CLI User Guide
==================

PIB CLI Internal Commands
-------------------------

This commands allow you to introspect the pib_cli application itself:

.. click:: pib_cli.cli.interface.builtins:builtin_commands
    :prog: dev @pib
    :nested: full

PIB CLI Default Custom Commands
-------------------------------

These are the default configuration based commands shipped with pib_cli:

.. click:: pib_cli.cli.interface.custom:defined_with_user_configuration
    :prog: dev
    :nested: full


PIB CLI Default Configuration
-----------------------------

The default YAML CLI configuration:

.. include:: ../../../pib_cli/config/default_cli_config.yml
   :literal:


PIB CLI Configuration JSON Schema
---------------------------------

Follow this schema to build your own CLI commands:

.. jsonschema:: ../../../pib_cli/config/schema.json
