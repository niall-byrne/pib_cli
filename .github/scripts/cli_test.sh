#!/bin/bash

# .github/scripts/cli_test.sh
# Validate the installed pib_cli version and built in configuration.

# CI only script.

set -eo pipefail

main() {

  PIB_CONFIG_FILE_LOCATION="$(pwd)/pib_cli/config/config.yml"

  dev build-wheel
  dev coverage
  dev fmt
  dev leaks
  dev lint
  dev reinstall-requirements
  dev sectest
  dev test

  [[ "$(dev @pib version)" =~ pib_cli[[:space:]]version:[[:space:]]1.[0-9]+.[0-9]+ ]]

  dev @pib config validate

  diff <(dev @pib config show) "${PIB_CONFIG_FILE_LOCATION}"
  [[ "$(dev @pib config where)" == "Current Configuration: ${PIB_CONFIG_FILE_LOCATION}" ]]

  dev @pib container setup
  [[ "$(dev @pib container version)" =~ Detected[[:space:]]PIB[[:space:]]container[[:space:]]version:[[:space:]]1\.[0-9]+\.[0-9]+ ]]

  set +e

  if [[ -f /etc/container_release ]]; then
    [[ "$(dev @pib container validate)" == "Detected valid container." ]] || exit 1
  else
    [[ "$(dev @pib container validate)" == "No PIB container found." ]] || exit 1
  fi

}

main "$@"
