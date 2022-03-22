CLI Reference
=============

There are two categories of `pib_cli` commands:

- internal commands
- customizable commands

While the internal commands are statically defined, you have complete control over the customizable commands.

`pib_cli` ships with some default customized commands that you can use with your project right away.


PIB CLI Internal Commands
-------------------------

These commands allow you to interact with the `pib_cli` application itself:

.. click:: pib_cli.cli.interface.builtins:builtin_commands
    :prog: dev @pib
    :nested: full

PIB CLI Default Custom Commands
-------------------------------

These are the default configuration based commands shipped with `pib_cli`:

.. click:: pib_cli.cli.interface.custom:document_custom_commands
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

.. jsonschema:: ../../../pib_cli/config/schemas/cli_base_schema_v2.1.0.json
.. jsonschema:: ../../../pib_cli/config/schemas/cli_cmd_schema_v0.1.0.json
