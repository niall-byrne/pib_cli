#!/bin/bash

# scripts/utilities/aspell_sort.sh
# Sort the aspell dictionary alphabetically and regenerate the header.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

main() {

  _WORD_COUNT="$(("$(wc -l .aspell.pws | cut -d"." -f1)" - 2))"
  _WORD_LIST="$(sed "1,1d" .aspell.pws | sort --unique)"
  _LANGUAGE="$(echo "${GIT_HOOKS_ASPELL_LANG}" | cut -d"_" -f1)"
  _HEADER="personal_ws-1.1 ${_LANGUAGE} ${_WORD_COUNT}"
  printf "%s\n%s\n" "${_HEADER}" "${_WORD_LIST}" > .aspell.pws

}

main "$@"
