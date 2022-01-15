# PIB CLI

A development environment CLI, complete with tooling.

[Project Documentation](https://pib_cli.readthedocs.io/en/latest/)

## Master Branch

[![pib_cli-automation](https://github.com/niall-byrne/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=master)](https://github.com/niall-byrne/pib_cli/actions)

## Production Branch

[![pib_cli-automation](https://github.com/niall-byrne/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=production)](https://github.com/niall-byrne/pib_cli/actions)

## Supported Python Versions

Tested to work under the following python version:
- Python 3.7
- Python 3.8
- Python 3.9

## Installation

This is a development environment CLI, with a customizable yaml config.

It's built into this [Cookie Cutter](https://github.com/cookiecutter/cookiecutter) template:

- [Python In A Box](https://github.com/niall-byrne/python-in-a-box)

To install, simply use: 
- `pip install pib_cli`
- `pip install pib_cli[docs]` (Adds [Sphinx](https://www.sphinx-doc.org/en/master/) support.)
- `pip install pib_cli[docstrings]` (Adds [pydocstyle](http://www.pydocstyle.org/en/stable/) support.)
- `pip install pib_cli[types]` (Adds [MyPy](http://mypy-lang.org/) support.)

## Usage

- use the `dev` command for details once installed

## Container

[python:3.7-slim](https://github.com/docker-library/python/tree/master/3.7/buster/slim)

## License

[MPL-2](LICENSE)

## Included Packages

After using `pib_cli` on a number of projects I realized there is not a one size fits all solution.  

- Some projects require extensive documentation, some projects require typing, some do not.
- At the suggestion of a friend, I've grouped the installable packages into "extras", that you can choose to install alongside the core `pib_cli` install.

### Core Installed Packages:
| package    | Description                       |
| ---------- | --------------------------------- |
| bandit     | Finds common security issues      |
| commitizen | Standardizes commit messages      |
| isort      | Sorts imports                     |
| poetry     | Python Package Manager            |
| pylint     | Static Code Analysis              |
| pytest     | Test suite                        |
| pytest-cov | Coverage support for pytest       |
| safety     | Dependency vulnerability scanning |
| wheel      | Package distribution tools        |
| yamllint   | Lint yaml configuration files     |
| yapf       | Customizable Code Formatting      |

- `poetry install` to install only these dependencies.
- This is the base install, and you'll always get these dependencies installed.

### 'docs' extras:
| package    | Description                       |
| ---------- | --------------------------------- |
| sphinx     | Generating documentation          |
| sphinx-autopackagesummary | Template nested module content |

- `poetry install -E docs` to add these dependencies to the core installation.

### 'docstrings' extras:
| package    | Description                       |
| ---------- | --------------------------------- |
| pydocstyle | PEP 257 enforcement               |

- `poetry install -E docstrings` to add these dependencies to the core installation.

### 'types' extras:
| package    | Description                       |
| ---------- | --------------------------------- |
| mypy       | Static type checker               |

- `poetry install -E types` to add these dependencies to the core installation.

### 'pib_docs' extras:
| package    | Description                       |
| ---------- | --------------------------------- |
| sphinx     | Generating documentation          |
| sphinx-autopackagesummary | Template nested module content     |
| sphinx-click              | Generate cli documentation         |
| sphinx-jsonschema         | Generate schema documentation      |

- `poetry install -E pib_docs` to add these dependencies to the core installation.
- These extras exist only to support building `pib_cli`'s documentation- they aren't meant to be consumed by user projects.

### Installing Multiple Extras:

This is straight-forward to do:
- `poetry install -E docs -E docstrings -E types`

## Customizing the Command Line Interface

The CLI has some defaults built in, but is customizable by setting the `PIB_CONFIG_FILE_LOCATION` environment variable.
The default config file can be found [here](pib_cli/config/config.yml).

Each command is described by a yaml key in this format :

```yaml
- name: "command-name"
  path_method: "location_string"
  commands:
    - "one or more"
    - "shell commands"
    - "each run in a discrete environment"
  success: "Success Message"
  failure: "Failure Message"
```

where `location_string` is one of:

- `project_root` (`/app`)
- `project_docs` (`/app/documentation`)
- `project_home` (`/app/${PROJECT_HOME}`)

## Installing a virtual environment, and the CLI on your host machine

The [scripts/extras.sh](scripts/extras.sh) script does this for you.

First install [poetry](https://python-poetry.org/) on your host machine:
- `pip install poetry`

Then source this script, setup the extras, and you can use the `dev` command on your host:
- `source scripts/extras.sh`
- `pib_setup_hostmachine` (to install the poetry dependencies)  
- `dev --help` (to run the cli outside the container)

This is most useful for making an IDE like pycharm aware of what's installed in your project.

> It is still recommended to work inside the container, as you'll have access to the full managed python environment, 
> as well as any additional services you are running in containers.  

If you wish to use the cli outside the container for all tasks, [tomll](https://github.com/pelletier/go-toml) and [gitleaks](https://github.com/zricethezav/gitleaks) will also need to be installed, or the [cli.yml](./assets/cli.yml) configuration will need to be customized to remove these commands.

## Development Guide for `pib_cli`

Please see the documentation [here](./CONTRIBUTING.md).
