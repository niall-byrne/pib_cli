# PIB CLI

A development environment CLI, complete with tooling.

[Project Documentation](https://pib_cli.readthedocs.io/en/latest/)

## Develop Branch

[![pib_cli-automation](https://github.com/shared-vision-solutions/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=develop)](https://github.com/shared-vision-solutions/pib_cli/actions)

## Master Branch

[![pib_cli-automation](https://github.com/shared-vision-solutions/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=master)](https://github.com/shared-vision-solutions/pib_cli/actions)

## Installation

This is a development environment CLI, with a customizable yaml config.

It's built into this [Cookie Cutter](https://github.com/cookiecutter/cookiecutter) template:

- [Python In A Box](https://github.com/shared-vision-solutions/python-in-a-box)

To install, simply use: `pip install pib_cli`

## Usage

- use the `dev` command for details once inside the container

## Container

[python:3.7-slim](https://github.com/docker-library/python/tree/master/3.7/buster/slim)

## License

[MPL-2](LICENSE)

## Installed Packages:
| package    | Description                       |
| ---------- | --------------------------------- |
| bandit     | Finds common security issues      |
| commitizen | Standardizes commit messages      |
| isort      | Sorts imports                     |
| poetry     | Python Package Manager            |
| pylint     | Static Code Analysis              |
| pytest     | Test suite                        |
| pytest-cov | Coverage support for pytest       |
| sphinx     | Generating documentation          |
| safety     | Dependency vulnerability scanning |
| wheel      | Package distribution tools        |
| yamllint   | Lint yaml configuration files     |
| yapf       | Customizable Code Formatting      |

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

Then source this script, setup the hostmachine, and you can use the `dev` command on your host:
- `source scripts/extras.sh`
- `pib_setup_hostmachine` (to install the poetry dependencies)  
- `dev --help` (to run the cli outside the container)

It is still recommended to work inside the container, as you'll have access to the full managed python environment, 
as well as any additional services you are running in containers.

## Development Dependencies

You'll need to install:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup the Development Environment

Build the development environment container (this takes a few minutes):

- `docker-compose build`

Start the environment container:

- `docker-compose up -d`

Spawn a shell inside the container:

- `./container`
