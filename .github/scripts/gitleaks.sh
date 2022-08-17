#!/bin/bash

# .github/scripts/gitleaks.sh
# Scan a range of commits for leaked secrets with gitleaks.

# CI only script, requires the jq binary to be present.

set -eo pipefail

main() {

  COUNT="$(echo "${PUSHED_COMMITS}" | jq length)"

  echo "Scanning ${COUNT} commit(s) ..."

  gitleaks detect --redact -s . --log-opts="HEAD~${COUNT}..HEAD"

}

main
