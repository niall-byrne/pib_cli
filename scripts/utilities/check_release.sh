#!/bin/bash

# scripts/utilities/check_release.sh
# Perform a series of release validation tests.

# Host machine only:  Please do not use this script inside a PIB container.

halt() {
  # $1 - Message

  echo "$1"
  exit 127
}

# Release Tests

set -eo pipefail

# Container
echo "Checking for container ..."
./scripts/hooks/check_container.sh

# Formatting
echo "Checking formatting ..."
./scripts/hooks/check_formatting.sh

# Add Additional Checks Here >

echo "Release Looks Good."
