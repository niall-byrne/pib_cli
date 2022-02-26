#!/bin/bash

# check_formatting.sh
# Check the code formatters do not create an unexpected diff.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

formatting_check() {

  dev fmt > /dev/null 2>&1

  if ! git diff --exit-code; then
    echo -e "\\nWARNING: code formatting needs to be checked!\\n"
    exit 127
  fi

}

main() {

  formatting_check "$@"

}

main "$@"
