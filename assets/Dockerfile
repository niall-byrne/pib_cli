FROM python:3.7-slim AS base
MAINTAINER niall@niallbyrne.ca
ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "pib_cli"
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

# Copy the codebase
COPY . /app

# Create the runtime user, and enforce permissions
RUN useradd user -d /home/user        \
                 -s /bin/bash         \
                 -M                   \
 && chown -R user:user /home/user     \
 && chown -R user:user /app

# ======================================================

# Development Environment
FROM base AS development
LABEL ENVIRONMENT=DEVELOPMENT
ENV ENVIRONMENT=DEVELOPMENT

# Install Dev Dependencies
RUN apt-get install -y     \
    curl                   \
    jq                     \
    openssh-client         \
    shellcheck             \
    sudo                   \
    tig                    \
    vim

# Add user to sudoers, and make the default user
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set the runtime user
USER user

# Setup The Dev CLI
RUN python setup.py install --user                    && \
    /home/user/.local/bin/dev setup-bash              && \
    /home/user/.local/bin/dev reinstall-requirements


CMD ["./pib_cli/container_init.sh"]
