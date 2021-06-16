# PIB CLI Development Guide

A development environment CLI, complete with tooling.

[Project Documentation](https://pib_cli.readthedocs.io/en/latest/)

## Development Dependencies

You'll need to install:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup the Development Environment

Build the development environment container (this takes a few minutes):

- `docker-compose build --build-arg PYTHON_VERSION=[3.7|3.8|3.9]`

Start the environment container:

- `docker-compose up -d`

Spawn a shell inside the container:

- `./container`
