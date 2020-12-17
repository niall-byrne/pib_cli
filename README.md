# Project Documentation

## PIB CLI

CLI for Python in a Box

### Develop Branch
[![pib_cli-automation](https://github.com/niall-byrne/python-in-a-box-cli/workflows/pib_cli%20Automation/badge.svg?branch=develop)](https://github.com/niall-byrne/python-in-a-box-cli/actions)

### Master Branch
[![pib_cli-automation](https://github.com/niall-byrne/python-in-a-box-cli/workflows/pib_cli%20Automation/badge.svg?branch=master)](https://github.com/niall-byrne/python-in-a-box-cli/actions)

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

## Development Tooling

- `$ dev` for details once inside the container

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