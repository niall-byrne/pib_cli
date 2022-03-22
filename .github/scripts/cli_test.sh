#!/bin/bash

# .github/scripts/cli_test.sh
# Validate the installed pib_cli version and built in configuration.

# CI only script.

set -eo pipefail

main() {

  PIB_CONFIG_FILE_LOCATION="$(pwd)/pib_cli/config/default_cli_config.yml"
  DEFAULT_CONFIG_WARNING="\*\* PIB DEFAULT CONFIG IN USE \*\*"

  dev build-wheel
  dev coverage
  dev fmt
  dev lint
  dev reinstall-requirements
  dev sectest
  dev test

  dev -h | grep "${DEFAULT_CONFIG_WARNING}"

  dev @pib version | grep -E "pib_cli version: 1.[0-9]+.[0-9]+"

  dev @pib config validate | grep "This configuration is valid."

  diff <(dev @pib config show | grep -v "${DEFAULT_CONFIG_WARNING}") "${PIB_CONFIG_FILE_LOCATION}"

  dev @pib config where | grep "Configuration file: ${PIB_CONFIG_FILE_LOCATION}"

  dev @pib container setup | grep "Setup Succeeded!"

  dev @pib container version | grep -E 'Container version: 1\.[0-9]+\.[0-9]+'

  set +e

  if [[ -f /etc/container_release ]]; then
    dev @pib container validate | grep "This container is valid."
  else
    dev @pib container validate | grep "No PIB container found."
  fi

}

main "$@"
