#!/bin/bash

# container_check.sh
# Encourage the user to make commits inside the managed development container.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

container_check() {

  if ! dev @pib container validate; then
    echo -e "\\nWARNING: please make commits inside the development container!\\n"
    exit 127
  fi

}

main() {

  container_check "$@"

}

main "$@"
