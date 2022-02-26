#!/bin/bash

# check_config.sh
# Check that the onboard configuration and base configuration match as expected.

set -eo pipefail

config_check() {

  set +e
  DIFF=$(diff assets/cli.yml pib_cli/config/config.yml)
  set -e

  EXPECTED=$(cat << EOF
3,11d2
< - name: "babel-extract"
<   description: "Create an updated template file for translations."
<   path: "git_root"
<   commands:
<     - "pybabel extract pib_cli/ -o pib_cli/config/locale/base.pot --omit-header"
<     - "pybabel update --omit-header -i pib_cli/config/locale/base.pot -o pib_cli/config/locale/en/LC_MESSAGES/base.po -l en -N"
<     - "pybabel compile -f -i ./pib_cli/config/locale/en/LC_MESSAGES/base.po -o ./pib_cli/config/locale/en/LC_MESSAGES/base.mo"
<   success: "Template and English translation base generated!"
<   failure: "An error occurred!"
16,19c7
<     - if [ ! -d "./source/codebase/\${PROJECT_NAME}/\${PROJECT_NAME}/_autosummary" ]; then rm -rf "./source/codebase/\${PROJECT_NAME}/\${PROJECT_NAME}/_autosummary"; fi
<     - "make gettext"
<     - "sphinx-intl update -p build/gettext -l en"
<     - make -e SPHINXOPTS="-D language='en'" html
---
>     - "make html"
43,47d30
<     - |
<       cat .aspell.pws | tail -n +2 | sort --unique > .aspell.pws.swp
<       sed "1s/^/personal_ws-1.1 en \$(wc -l .aspell.pws.swp | awk '{print \$1}')\n/" .aspell.pws.swp > .aspell.pws
<       rm .aspell.pws.swp
<     - 'tomll pyproject.toml'
61d43
<   description: "Run the code linters."
62a45
>   description: "Run the code linters."
64,65c47
<     - 'shellcheck \${PROJECT_NAME}/bash/* -x'
<     - 'shellcheck \${PROJECT_NAME}/container_init.sh'
---
>     - 'yamllint *.yml .*.yml assets/ .github/workflows/'
69d50
<     - 'yamllint *.yml .*.yml \${PROJECT_NAME}/config/ assets/ .github/workflows/'
79c60
<     - "poetry install -E pib_docs"
---
>     - "poetry install -E docs"
88c69
<     - 'poetry export --without-hashes -f requirements.txt | safety check --stdin -i 41002'
---
>     - 'poetry export --without-hashes -f requirements.txt | safety check --stdin'
EOF
)

  if [[ "${DIFF}" != "${EXPECTED}" ]]; then
    echo -e "\\nWARNING: the onboard configuration no longer matches the customized configuration!\\n"
    exit 127
  fi

}

main() {

  config_check "$@"

}

main "$@"
