ARG BUILD_ARG_PYTHON_VERSION=3.7
FROM python:$BUILD_ARG_PYTHON_VERSION-slim AS base

ARG BUILD_ARG_ASPELL_LANGUAGE="en"

LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pib_cli"
LABEL environment="stage1"

ENV PYTHONUNBUFFERED "1"
ENV PIB_PROJECT_NAME "pib_cli"
ENV PIB_CONFIG_FILE_LOCATION "/app/assets/cli.yml"

ENV VERSION_ASPELL "aspell-${BUILD_ARG_ASPELL_LANGUAGE}=*"
ENV VERSION_GITLEAKS "8.3.0"
ENV VERSION_POETRY "poetry<1.4.0"

# Mark Container
RUN echo "1.0.0" > /etc/container_pib_version   && \
    echo "pib_cli" > /etc/container_release

# Install Base Dependencies
RUN apt-get update               && \
    apt-get upgrade -y           && \
    apt-get install -y              \
    --no-install-recommends         \
    bash=5.*                        \
    build-essential=12.*         && \
    rm -rf /var/lib/apt/lists/*

# Setup directories
RUN mkdir -p /home/user /app
WORKDIR /app

# Create the runtime user, and enforce permissions
RUN useradd user -d /home/user        \
                 -s /bin/bash         \
                 -M                   \
 && chown -R user:user /home/user     \
 && chown -R user:user /app

ENV PATH "/home/user/.local/bin/:${PATH}"

# ======================================================

# Poetry Intermediary
FROM base AS poetry

LABEL environment="stage2"

# Install Latest Poetry
# hadolint ignore=DL3013
RUN pip install --no-cache-dir "${VERSION_POETRY}"

# ======================================================

# Development Environment
FROM poetry AS development
LABEL environment="DEVELOPMENT"
ENV ENVIRONMENT DEVELOPMENT

# Install Dev Dependencies
# hadolint ignore=DL3008
RUN apt-get update                      && \
    apt-get install -y                     \
    --no-install-recommends                \
    "${VERSION_ASPELL}"                    \
    curl=7.74.*                            \
    fish=3.1.*                             \
    golang-github-pelletier-go-toml=1.8.*  \
    jq=1.6*                                \
    openssh-client=1:8.*                   \
    pandoc=2.*                             \
    shellcheck=0.7.*                       \
    sudo=1.9.*                             \
    tig=2.5.*                              \
    vim=2:8.*

# Install Git Leaks
COPY ./scripts/utilities/install_gitleaks.sh .
RUN bash -c 'source install_gitleaks.sh'  && \
    rm install_gitleaks.sh

# Add user to sudoers, and make the default user
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set the runtime user
USER user

# Copy the poetry configuration
COPY pyproject.toml /app/

# Cache Dependencies
RUN poetry install --no-root -E docstrings -E docs -E types -E pib_docs

# Copy the codebase
COPY . /app

# Create A Symlink For the Bash Customizations
RUN ln -sf /app/assets/.bash_customize /home/user/.bash_customize

# Modify the git hooks permissions
USER root
RUN chown user /app/.git/hooks/*
USER user

# Setup The Dev CLI, bootstrapping the current version of pib_cli
RUN poetry install -E docstrings -E docs -E types -E pib_docs         && \
    poetry run dev @pib container setup                               && \
    poetry run pre-commit install

CMD ["./pib_cli/container_init.sh"]

# ======================================================

# Pre Production Environment
FROM poetry as pre_production

LABEL environment="PRE_PRODUCTION"

ENV ENVIRONMENT "PRE_PRODUCTION"

# Set the runtime user
USER user

# Copy the poetry configuration
COPY pyproject.toml /app/

# Export the lock file
RUN poetry lock    && \
    poetry export --without-hashes -E docstrings -E pib_docs -E types -f requirements.txt -o /app/requirements.txt

# Copy the codebase
COPY . /app

# ======================================================

# Production Environment
FROM base as production

LABEL environment="PRODUCTION"

ENV ENVIRONMENT "PRODUCTION"

# Set the runtime user
USER user

# Copy the requirements.txt file from pre_production
COPY --from=pre_production /app/requirements.txt /app/requirements.txt

# Install Production Packages Only
RUN pip --no-cache-dir install -r requirements.txt

# Copy the codebase
COPY . /app

CMD ["./{{cookiecutter.project_slug}}/container_init.sh"]
