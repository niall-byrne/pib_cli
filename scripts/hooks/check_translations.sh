#!/bin/bash

# check_translations.sh
# Check there has not been changes to the translation content.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

restore_config() {
    PIB_CONFIG_FILE_LOCATION="${ORIGINAL_PIB_CONFIG_FILE_LOCATION}"
  }

check_python_translations() {
  dev babel-extract > /dev/null 2>&1
}

check_sphinx_translations() {
  pushd documentation > /dev/null 2>&1 || exit 127
    make gettext > /dev/null 2>&1
    sphinx-intl update -p build/gettext -l en > /dev/null 2>&1
  popd > /dev/null 2>&1
}

translation_check() {

  # Use the default configuration for all translation operations
  PIB_CONFIG_FILE_LOCATION="$(git rev-parse --show-toplevel)/pib_cli/config/default_cli_config.yml"

  check_python_translations &
  check_sphinx_translations &

  wait

  if ! git diff --exit-code documentation/source/locale/en/LC_MESSAGES/*.po pib_cli/config/locale/en/LC_MESSAGES/base.po; then
    echo -e "\\nWARNING: there has been a change to the translation content detected!\\n"
    exit 127
  fi

}

main() {

  ORIGINAL_PIB_CONFIG_FILE_LOCATION="${PIB_CONFIG_FILE_LOCATION}"
  trap restore_config EXIT

  translation_check "$@"

}

main "$@"
