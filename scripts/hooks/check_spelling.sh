#!/bin/bash

# check_spelling.sh
# Run aspell on the commit content using a personal dictionary.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

spell_check() {

  USER_DICTIONARY="$(git rev-parse --show-toplevel)/.aspell.pws"
  COMMIT_MESSAGE=$(sed '/Please enter the commit message for your changes./q' "${1}" | head -n -1)
  ERRORS=$(echo "${COMMIT_MESSAGE}" | aspell --encoding="${GIT_HOOKS_ASPELL_ENCODING}" --personal="${USER_DICTIONARY}" --lang="${GIT_HOOKS_ASPELL_LANG}" -t --list)

  if [ -n "${ERRORS}" ]; then
    echo "YOUR COMMIT MESSAGE:"
    echo "${COMMIT_MESSAGE}"
    echo -e "\\nWARNING: possible spelling error in commit message:\\n"
    echo -e "${ERRORS}\\n"
    echo -e "(You may wish to add these words to the local '.aspell.pws' file.)\\n"
    exit 127
  fi

}

main() {

  spell_check "$@"

}

main "$@"
