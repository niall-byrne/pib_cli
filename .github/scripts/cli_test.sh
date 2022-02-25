#!/bin/bash

set -eo pipefail

main() {

  dev build-docs
  dev build-wheel
  dev coverage
  dev fmt
  dev leaks
  dev lint
  dev reinstall-requirements
  dev sectest
  dev test
  dev types

  dev @pib version

  dev @pib config validate
  diff <(echo "Current Configuration: ${PIB_CONFIG_FILE_LOCATION}") <(dev @pib config where)
  diff <(dev @pib config show) "${PIB_CONFIG_FILE_LOCATION}"

  dev @pib container version
  dev @pib container setup

}

main "$@"
