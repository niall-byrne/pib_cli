#!/bin/bash

set -eo pipefail

main() {

  echo "CHANGE_LOG<<EOF" >> "${GITHUB_ENV}"
  cz ch --start-rev "$(git tag | sort -V | tail -n2 | head -n1)" --dry-run >> "$GITHUB_ENV"
  echo "EOF" >> "${GITHUB_ENV}"

}

main "$@"
