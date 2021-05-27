#!/bin/bash

set -o pipefail

main() {

  shellcheck ./.github/scripts/*.sh
  shellcheck ./pib_cli/*.sh
  shellcheck ./scripts/*.sh
  shellcheck ./scripts/hooks/*

}

main "$@"
