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
7d6
<     - 'if [ ! -d "./source/codebase/\${PROJECT_NAME}/\${PROJECT_NAME}/_autosummary" ]; then rm -rf "./source/codebase/\${PROJECT_NAME}/\${PROJECT_NAME}/_autosummary"; fi'
32,36d30
<     - |
<       cat .aspell.pws | tail -n +2 | sort --unique > .aspell.pws.swp
<       sed "1s/^/personal_ws-1.1 en \$(wc -l .aspell.pws.swp | awk '{print \$1}')\n/" .aspell.pws.swp > .aspell.pws
<       rm .aspell.pws.swp
<     - 'tomll pyproject.toml'
50d43
<   description: "Run the code linters."
51a45
>   description: "Run the code linters."
53,54c47
<     - 'shellcheck \${PROJECT_NAME}/bash/* -x'
<     - 'shellcheck \${PROJECT_NAME}/container_init.sh'
---
>     - 'yamllint *.yml .*.yml assets/ .github/workflows/'
58d50
<     - 'yamllint *.yml .*.yml \${PROJECT_NAME}/config/ assets/ .github/workflows/'
68c60
<     - "poetry install -E pib_docs"
---
>     - "poetry install -E docs"
77c69
<     - 'poetry export --without-hashes -f requirements.txt | safety check --stdin -i 41002'
---
>     - 'poetry export --without-hashes -f requirements.txt | safety check --stdin'
91,93c83,85
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
