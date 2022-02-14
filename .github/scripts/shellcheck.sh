#!/bin/bash

set -eo pipefail

main() {

  shellcheck ./.github/scripts/*.sh
  shellcheck ./pib_cli/*.sh
  shellcheck ./scripts/*.sh
  shellcheck ./scripts/hooks/*.sh

}

main "$@"
