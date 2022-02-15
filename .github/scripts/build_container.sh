#!/bin/bash

set -eo pipefail

main() {

  docker-compose build --build-arg BUILD_ARG_PYTHON_VERSION="${PYTHON_VERSION}"
  docker-compose up -d

}

main "$@"
