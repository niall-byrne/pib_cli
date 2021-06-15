#!/bin/bash

halt() {
  # $1 - Message

  echo "$1"
  exit 127
}

# Release Tests
[[ ! -f /etc/container_release ]] && halt "Must be run inside the container."

# Formatting
echo "Checking Formatting ... "
dev fmt
DIFF=$(git diff)
[[ -n "${DIFF}" ]] && halt "Formatting needs to be checked!"

# Config
echo "Checking Config ... "
DIFF=$(diff assets/cli.yml pib_cli/config/config.yml)
EXPECTED=$(cat << EOF
28d27
<     - 'tomll pyproject.toml'
43,45c42
<     - 'shellcheck \${PROJECT_NAME}/bash/* -x'
<     - 'shellcheck \${PROJECT_NAME}/container_init.sh'
<     - 'yamllint *.yml .*.yml \${PROJECT_NAME}/config/ assets/ .github/workflows/'
---
>     - 'yamllint *.yml .*.yml assets/ .github/workflows/'
54c51
<     - "poetry install -E pib_docs"
---
>     - "poetry install -E docs"
74,76c71,73
<     - 'echo "Typing is disabled for this project."'
<   success: ""
<   failure: ""
---
>     - 'mypy \${PROJECT_NAME}'
>   success: "Type Check Passed!"
>   failure: "Type Check Failed!"
EOF
)
[[ "${DIFF}" != "${EXPECTED}" ]] && halt "Assets and Onboard CLI configuration does not appear to match."

echo "Release Looks Good."
