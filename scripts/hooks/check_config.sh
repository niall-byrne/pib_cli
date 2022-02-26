#!/bin/bash

# check_config.sh
# Check that the onboard configuration and project configuration match as expected.

# Generate new diff Content: diff assets/cli.yml pib_cli/config/config.yml > ./assets/config_drift.diff

set -eo pipefail

config_check() {

  GIT_ROOT="$(git rev-parse --show-toplevel)"
  DIFF_EXPECTED=$(cat "${GIT_ROOT}/assets/config_drift.diff")

  set +e
  DIFF_CURRENT=$(diff "${GIT_ROOT}/assets/cli.yml" "${GIT_ROOT}/pib_cli/config/config.yml")
  set -e

  if [[ "${DIFF_CURRENT}" != "${DIFF_EXPECTED}" ]]; then
    echo -e "\\nWARNING: the onboard configuration no longer matches the customized configuration!\\n"
    exit 127
  fi

}

main() {

  config_check "$@"

}

main "$@"
