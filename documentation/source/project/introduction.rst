PIB CLI
=======

A batteries included `make <https://www.gnu.org/software/make/>`__ style CLI for
`python <https://python.org>`__ projects in `git <https://git-scm.com/>`__ repositories.

`Project Documentation <https://pib-cli.readthedocs.io/en/latest/>`__

Master Branch
-------------

|pib_cli-automation-master|

Production Branch
-----------------

|pib_cli-automation-production|

Documentation Builds
--------------------

|Documentation Status|

Supported Python Versions
-------------------------

Tested to work with the following Python versions:

-  Python 3.7 (minimum 3.7.2)
-  Python 3.8
-  Python 3.9
-  Python 3.10

Installation
------------

To install, simply use:

-  ``pip install pib_cli``
-  ``pip install pib_cli[docs]`` (Adds `Sphinx <https://www.sphinx-doc.org/en/master/>`__ support.)
-  ``pip install pib_cli[docstrings]`` (Adds `pydocstyle <http://www.pydocstyle.org/en/stable/>`__
   support.)
-  ``pip install pib_cli[types]`` (Adds `mypy <http://mypy-lang.org/>`__ support.)

Usage
-----

-  The CLI itself is launched with the ``dev`` command.
-  Try ``dev --help`` for details.

With Cookiecutter
-----------------

``pib_cli`` is also baked into this `Cookie Cutter <https://github.com/cookiecutter/cookiecutter>`__
template:

-  `Python In A Box <https://github.com/niall-byrne/python-in-a-box>`__

License
-------

`MPL-2 <https://github.com/niall-byrne/pib_cli/blob/master/LICENSE>`__

Included Packages
-----------------

As it’s batteries included, ``pib_cli`` ships with a slightly opinionated list of popular
development packages. You can customize the exact mix by specifying one or more
`extras <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/?highlight=extras#installing-extras>`__
when installing the package.

Core installed packages
~~~~~~~~~~~~~~~~~~~~~~~

============= =================================
package       Description
============= =================================
bandit        Finds common security issues
commitizen    Standardizes commit messages
isort         Sorts imports
pre-commit    Pre-commit hook manager
pylint        Static code analysis
pytest        Testing with Python
pytest-cov    Coverage support for pytest
pytest-pylint Pylint support for pytest
safety        Dependency vulnerability scanning
wheel         Package distribution tools
yamllint      Lint YAML configuration files
yapf          Customizable code formatting
============= =================================

Installed and required by pib_cli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

========== ==================================
package    Description
========== ==================================
click      Command line interface toolkit
jsonschema JSON Schema validation for Python
GitPython  Interact with Git repositories
PyYAML     YAML parser and emitter for Python
========== ==================================

-  ``pip install pib_cli`` to install only these dependencies.
-  These become indirect **development** dependencies of **YOUR** project, so it’s good to keep that
   in mind.

‘docs’ extras
~~~~~~~~~~~~~

========================= =============================================================
package                   Description
========================= =============================================================
darglint                  Sphinx style guide enforcement
sphinx                    Python documentation generator
sphinx-autopackagesummary Template nested module content
sphinx_rtd_theme          The `Read the Docs <https://readthedocs.org/>`__ Sphinx theme
========================= =============================================================

-  ``pip install pib_cli[docs]`` to add these dependencies to the core installation.

‘docstrings’ extras
~~~~~~~~~~~~~~~~~~~

========== ===================
package    Description
========== ===================
pydocstyle PEP 257 enforcement
========== ===================

-  ``pip install[docstrings]`` to add these dependencies to the core installation.

‘types’ extras
~~~~~~~~~~~~~~

======= ===================
package Description
======= ===================
mypy    Static type checker
======= ===================

-  ``pip install pib_cli[types]`` to add these dependencies to the core installation.

‘pib_docs’ extras
~~~~~~~~~~~~~~~~~

========================= =============================================================
package                   Description
========================= =============================================================
sphinx                    Python documentation generator
sphinx-autopackagesummary Templates nested module content
sphinx-click              Generates CLI documentation
sphinx-intl               Generates documentation translations
sphinx-jsonschema         Generates JSON schema documentation
sphinx_rtd_theme          The `Read the Docs <https://readthedocs.org/>`__ Sphinx theme
========================= =============================================================

-  ``pip install pib_cli[pib_docs]`` to add these dependencies to the core installation.
-  These extras exist only to support building ``pib_cli`` documentation- they aren’t meant to be
   consumed by user projects.

Installing multiple extras
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is straightforward to do:

-  ``pip install pib_cli[docs,docstrings,types]``

Customizing the Command Line Interface
--------------------------------------

The most powerful feature of ``pib_cli`` is its ability to customize how it interacts with the
packages it brings to your project. In this way it’s very similar to the standard Linux
`make <https://www.gnu.org/software/make/>`__ command- with the notable difference being that
``pib_cli`` is packaged with a suite of Python libraries.

**The CLI configuration file is in YAML format, and conforms
to**\ `this <https://github.com/niall-byrne/pib_cli/blob/master/pib_cli/config/schemas>`__\ **set of
JSON schemas.**

-  pib_cli v1.0.0 introduces a `new JSON schema
   version <https://github.com/niall-byrne/pib_cli/blob/master/pib_cli/config/schemas/cli_base_schema_v2.0.0.json>`__.
-  pib_cli v1.2.0 introduces `further refinements to the JSON
   schema <https://github.com/niall-byrne/pib_cli/blob/master/pib_cli/config/schemas/cli_base_schema_v2.1.0.json>`__
   but is fully backwards compatible with v1.0.0, and **ALL** legacy configuration files.

Creating a ‘.pib.yml’ file
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``.pib.yml`` file is where you can take control, and customize ``pib_cli`` behaviour to suit
your particular needs. This file should adhere to the specification detailed above- read on for
further detail.

The top level of your ``.pib.yml`` file should include metadata information. This metadata is used
to tell ``pib_cli`` where to find your project’s codebase and any documentation (Sphinx)
definitions.

.. code:: yaml

   metadata:
     project_name: "Tell pib_cli the folder your codebase is in."
     documentation_root: "Tell pib_cli where to find your documentation definitions."
   cli_definition:
     - [A YAML array of cli command definitions, which are detailed in the next section].

-  The ``cli_definition`` section is mandatory, and ``pib_cli`` will throw an error if it’s missing.
-  The metadata itself though is actually optional, and can also be declared using environment
   variables.

**Understanding pib_cli metadata**

Metadata tells ``pib_cli`` where to find your project’s files, so it’s important to set these values
appropriately:

-  ``project_name`` is your project’s name from a Python perspective. It’s the top level folder
   (inside your git repository) that houses your codebase, such that
   ``from <project_name> import *`` would be accessing your codebase.
-  ``documentation_root`` is a relative path from your repository’s root to a folder containing a
   Sphinx Makefile. This is purely a convenience definition for any documentation related commands.

**Environment variables and pib_cli**

You may also define your project’s metadata by setting environment variables. This would allow you
to reuse the same CLI configuration for multiple projects:

-  ``project_name`` can also be defined by ``PIB_PROJECT_NAME`` environment variable
-  ``documentation_root`` can also be defined by the ``PIB_DOCUMENTATION_ROOT`` environment variable

When configuration AND environment variables exist, ``pib_cli`` will **prefer to use environment
variable values**.

**Environment variables and pib_cli commands**

Regardless of whether you have used configuration or environment variables, when your CLI commands
are executed, the environment variables will be available in the shell:

-  ``PIB_PROJECT_NAME`` will always be defined and accessible from inside the shell
-  ``PIB_DOCUMENTATION_ROOT`` will always be defined and accessible from inside the shell

Adding a CLI definition to a ‘.pib.yml’ file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``cli_definition`` YAML key, should contain a list of definitions for CLI commands you wish to
use.

Each command should adhere to this format (and you can have many commands for whatever tasks you
need to perform):

.. code:: yaml

       - name: "command-name"
         description: "A description of the command."
         container_only: false # Optional restriction of the command to a PIB container
         path: "repo_root"
         commands:
           - "one or more"
           - "shell commands"
           - "each run in a discrete environment"
           - "The ${PIB_DOCUMENTATION_ROOT} environment variable is also available if you need to navigate to that folder."
           - "The ${PIB_PROJECT_NAME} environment variable is available if you need to navigate to that folder."
           - "Any extra arguments passed are stored in the ${PIB_OVERLOAD_ARGUMENTS} environment variable."
         success: "Success Message"
         failure: "Failure Message"

Notes on this configuration format:

-  ``container_only`` restricts the command to working only inside a
   `Python-in-a-Box <https://github.com/niall-byrne/python-in-a-box>`__ container environment.
   (Completely optional key to include, defaults to ``false``.)
-  ``path`` must be one of:

   -  ``repo_root`` (The root folder of your code repository.)
   -  ``documentation_root`` (Defaults to the folder ``documentation``, can be customized with
      metadata or environment variables.)
   -  ``project_root`` (The ``project_name`` folder as defined with metadata or environment
      variables.)

Validating a ‘.pib.yml’ file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``pib_cli`` to validate new configuration files before activating them:

-  ``dev @pib config -c <path to your file> validate``

Activating a ‘.pib.yml’ file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To ``activate`` your configuration, use one of the following methods:

1. You can set the environment variable ``PIB_CONFIG_FILE_LOCATION`` to the absolute path where the
   file is located.
2. Or just move your new ``.pib.yml`` file to the top level folder (the repository root) of your
   project.

Use the command ``dev @pib config where`` to confirm it’s been activated.

If a ``.pib.yml`` file cannot be found with either of these methods, then the `default
config <https://github.com/niall-byrne/pib_cli/blob/master/pib_cli/config/default_cli_config.yml>`__
will be used.

Development Guide for ``pib_cli``
---------------------------------

Please see the documentation
`here <https://github.com/niall-byrne/pib_cli/blob/master/CONTRIBUTING.md>`__.

Environment Variable Summary
----------------------------

This table summarizes the environment variables that can be used with ``pib_cli``:

======================== =======================================================================
Name                     Purpose
======================== =======================================================================
PIB_CONFIG_FILE_LOCATION The absolute path to the configuration file that should be used.
PIB_DOCUMENTATION_ROOT   A relative path from the repository root where a Sphinx Makefile lives.
PIB_OVERLOAD_ARGUMENTS   Reserved to pass arguments to customized CLI commands.
PIB_PROJECT_NAME         The top level folder in the repository where the codebase is found.
======================== =======================================================================

.. |pib_cli-automation-master| image:: https://github.com/niall-byrne/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=master
   :target: https://github.com/niall-byrne/pib_cli/actions
.. |pib_cli-automation-production| image:: https://github.com/niall-byrne/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=production
   :target: https://github.com/niall-byrne/pib_cli/actions
.. |Documentation Status| image:: https://readthedocs.org/projects/pib-cli/badge/?version=latest
   :target: https://pib-cli.readthedocs.io/en/latest/?badge=latest
