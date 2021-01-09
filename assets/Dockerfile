FROM python:3.7-slim AS base
MAINTAINER niall@niallbyrne.ca
ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "pib_cli"
ENV PIB_CONFIG_FILE_LOCATION "/app/assets/cli.yml"
ENV POETRY_VIRTUALENVS_CREATE "false"
LABEL PROJECT=pib_cli

# Mark Container
RUN echo "pib_cli" > /etc/container_release

# Install Base Dependencies
RUN apt-get update      && \
    apt-get upgrade -y  && \
    apt-get install -y     \
    bash                   \
    build-essential

# Setup directories
RUN mkdir -p /home/user /app
WORKDIR /app

# Create the runtime user, and enforce permissions
RUN useradd user -d /home/user        \
                 -s /bin/bash         \
                 -M                   \
 && chown -R user:user /home/user     \
 && chown -R user:user /app

# Install Latest Poetry
RUN pip install poetry

ENV PATH "/home/user/.local/bin/:${PATH}"

# ======================================================

# Development Environment
FROM base AS development
LABEL ENVIRONMENT=DEVELOPMENT
ENV ENVIRONMENT=DEVELOPMENT

# Install Dev Dependencies
RUN apt-get install -y              \
    curl                            \
    jq                              \
    golang-github-pelletier-go-toml \
    openssh-client                  \
    shellcheck                      \
    sudo                            \
    tig                             \
    vim

# Add user to sudoers, and make the default user
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Copy the codebase
COPY . /app

# Set the runtime user
USER user

# Setup The Dev CLI, bootstrapping the current version of pib_cli
RUN poetry install                                    && \
    dev setup-bash                                    && \
    dev reinstall-requirements

CMD ["./pib_cli/container_init.sh"]

# ======================================================

# Production Environment
FROM base as production
LABEL ENVIRONMENT=PRODUCTION
ENV ENVIRONMENT=PRODUCTION

# Copy the codebase
COPY . /app

# Install Production Packages Only
RUN poetry install --no-dev --no-root

# Set the runtime user
USER user

CMD ["./{{cookiecutter.project_slug}}/container_init.sh"]
