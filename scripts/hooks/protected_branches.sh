#!/bin/bash

# protected_branches.sh
# Run additional pre-commit checks on selected branches.

# Container Only:  Please use this hook inside a PIB container.

set -eo pipefail

bypass() {

  LOCAL_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  TARGET_BRANCHES="${GIT_HOOKS_PROTECTED_BRANCHES}"

  if [[ ! ${LOCAL_BRANCH} =~ ${TARGET_BRANCHES} ]]; then
        exit 0
  fi

}

protected_branches() {

  dev lint
  dev sectest
  dev test
  find scripts -type f -exec shellcheck -x "{}" \;

}

main() {

  bypass
  protected_branches

}

main "$@"
