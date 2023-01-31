#!/bin/bash

set -eo pipefail

main() {

  docker-compose build                              \
    --build-arg PYTHON_VERSION="${PYTHON_VERSION}"  \
    --build-arg CONTAINER_UID="$(id -u)"
  docker-compose up -d

}

main "$@"
