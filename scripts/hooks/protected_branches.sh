#!/bin/bash

# protected_branches.sh
# Run additional pre-commit checks on selected branches.

set -eo pipefail

bypass() {

  local_branch="$(git rev-parse --abbrev-ref HEAD)"
  protected_branches="${GIT_HOOKS_PROTECTED_BRANCHES}"

  if [[ ! ${local_branch} =~ ${protected_branches} ]]; then
        exit 0
  fi

}

checks() {

  dev lint
  dev sectest
  dev test
  find scripts -type f -exec shellcheck -x "{}" \;

}

main() {

  bypass
  checks

}

main "$@"
