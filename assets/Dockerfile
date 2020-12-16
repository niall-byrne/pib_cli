FROM python:3.7-slim AS base
MAINTAINER niall@niallbyrne.ca
ENV PYTHONUNBUFFERED 1
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

# Setup The Dev CLI, and Install all Packages
RUN scripts/commander.sh setup

CMD ["./pib_cli/container_init.sh"]

# ======================================================

# Production Environment
FROM base as production
LABEL ENVIRONMENT=PRODUCTION
ENV ENVIRONMENT=PRODUCTION

# Install Production Packages Only
RUN pip install -r /app/assets/requirements.txt

# Set the runtime user
USER user

CMD ["./pib_cli/container_init.sh"]
