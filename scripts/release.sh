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
6d5
<     - 'if [ ! -d "./source/codebase/\${PROJECT_NAME}/\${PROJECT_NAME}/_autosummary" ]; then rm -rf "./source/codebase/\${PROJECT_NAME}/\${PROJECT_NAME}/_autosummary"; fi'
28d26
<     - 'tomll pyproject.toml'
43,44c41
<     - 'shellcheck \${PROJECT_NAME}/bash/* -x'
<     - 'shellcheck \${PROJECT_NAME}/container_init.sh'
---
>     - 'yamllint *.yml .*.yml assets/ .github/workflows/'
47d43
<     - 'yamllint *.yml .*.yml \${PROJECT_NAME}/config/ assets/ .github/workflows/'
56c52
<     - "poetry install -E pib_docs"
---
>     - "poetry install -E docs"
64c60
<     - 'poetry export --without-hashes -f requirements.txt | safety check --stdin -i 41002'
---
>     - 'poetry export --without-hashes -f requirements.txt | safety check --stdin'
76,78c72,74
<     - 'echo "Typing is disabled for this project."'
<   success: ""
<   failure: ""
---
>     - 'mypy --strict \${PROJECT_NAME}'
>   success: "Type Check Passed!"
>   failure: "Type Check Failed!"
EOF
)
[[ "${DIFF}" != "${EXPECTED}" ]] && halt "Assets and Onboard CLI configuration does not appear to match."

echo "Release Looks Good."
