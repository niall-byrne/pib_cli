#!/bin/bash

# check_translations.sh
# Check there has not been changes to the translation content.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

translation_check() {

  dev babel-extract > /dev/null 2>&1

  pushd documentation > /dev/null 2>&1 || exit 127
    make gettext > /dev/null 2>&1
    sphinx-intl update -p build/gettext -l en > /dev/null 2>&1
  popd > /dev/null 2>&1

  if ! git diff --exit-code pib_cli/config/locale/en/LC_MESSAGES/base.po; then
    echo -e "\\nWARNING: there has been a change to the translation content detected!\\n"
    exit 127
  fi

}

main() {

  translation_check "$@"

}

main "$@"
