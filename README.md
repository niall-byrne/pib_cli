# Project Documentation

## PIB CLI

CLI for Python in a Box

[Project Documentation](https://pib_cli.readthedocs.io/en/latest/)

### Develop Branch
[![pib_cli-automation](https://github.com/niall-byrne/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=develop)](https://github.com/niall-byrne/pib_cli/actions)

### Master Branch
[![pib_cli-automation](https://github.com/niall-byrne/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=master)](https://github.com/niall-byrne/pib_cli/actions)

## Installation

This CLI is designed to be installed inside a project created by the [Cookie Cutter](https://github.com/cookiecutter/cookiecutter) template:
- [Python In A Box](https://github.com/niall-byrne/python-in-a-box)

To install, simply use: `pip install pib_cli`

## Usage

- use the `dev` command for details once inside the container

## Customizing the Command Line Interface

Configuring the CLI:

The CLI has some defaults built in, but is customizable by setting the `PIB_CONFIG_FILE_LOCATION` environment variable.

The config file itself is yaml.  
Each command is described by a yaml key in this format :
```yaml
- name: "command-name"
  path_method: "location_string"
  commands:
    - 'one or more'
    - 'shell commands'
    - 'each run in a discrete environment'
  success: "Success Message"
  failure: "Failure Message"
```

where `location_string` is one of:
- `project_root` (`/app`)
- `project_docs` (`/app/documentation`)
- `project_home` (`/app/${PROJECT_HOME}`)

## Installing a virtual environment on your host machine

The `scripts/hostmachine.sh` script does this for you.

It will use `pipenv` to create a virtual environment and install both requirements files in the assets folder.  
This is useful if you want to make your local IDE aware of what's installed.

(`pip install pipenv` or `brew install pipenv` may be necessary on your system.)

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