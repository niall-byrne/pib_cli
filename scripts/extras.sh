#!/bin/bash

ROOT="$(git rev-parse --show-toplevel)"

pib_setup_hostmachine() {
  poetry install -E docstrings -E pib_docs

  # shellcheck disable=SC2139
  alias dev="PIB_PROJECT_NAME=\"pib_cli\" PIB_CONFIG_FILE_LOCATION=\"${ROOT}/assets/cli.yml\" poetry run dev"
}
