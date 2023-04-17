# PIB CLI Development Guide

A batteries included [make](https://www.gnu.org/software/make/) style CLI for [python](https://python.org) projects in [git](https://git-scm.com/) repositories.

[Project Documentation](https://pib-cli.readthedocs.io/en/latest/)

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

## Environment Variables in the Dev Environment

Developing `pib_cli` is a bit of a chicken and egg problem, as the project makes use of itself during development.

To manage this, the `default config` is activated during the execution of tests, linting, etc.  You can see this [here](./assets/cli.yml).

## Deviations from PEP

I prefer to use a two-space indent, and so [yapf](https://github.com/google/yapf) is configured this way.  Please use the `dev fmt` command to match style on commits.
