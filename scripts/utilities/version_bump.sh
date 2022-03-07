#!/bin/bash

# scripts/utilities/version_bump.sh
# Increment the project's semantic version and create a Git tag.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

main() {

  _BUMP_TYPE="$(cz bump --dry-run)"
  _BUMP_TYPE="$(echo "${_BUMP_TYPE}" | grep increment | cut -d":" -f2 | tr '[:upper:]' '[:lower:]' | xargs)"
  poetry version "${_BUMP_TYPE}"
  git stage .
  cz bump

}

main "$@"
