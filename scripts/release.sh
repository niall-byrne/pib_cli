#!/bin/bash

halt() {
  # $1 - Message

  echo "$1"
  exit 127
}

# Release Tests
[[ ! -f /etc/container_release ]] && halt "Must be run inside the container."

# Formatting

set -eo pipefail

# Check Formatting
echo "Checking Formatting ..."
/app/scripts/hooks/check_formatting.sh

# Check Translations
echo "Checking Translations ..."
/app/scripts/hooks/check_translations.sh

# Check Configuration
echo "Checking Configuration ..."
/app/scripts/hooks/check_config.sh

echo "Release Looks Good."
