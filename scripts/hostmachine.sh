#!/bin/bash

set -e

ROOT="$(git rev-parse --show-toplevel)"
ARG="${1}"

conditional_source() {
  if ! pipenv --venv >/dev/null 2>&1; then
    setup_python
  fi
  spawn_shell
}

setup_python() {

  unvirtualize

  pushd "${ROOT}"  > /dev/null
    if [[ ! -f /etc/container_release ]]; then
      set +e
        pipenv --rm
      set -e
      pipenv --python 3.7
    fi
    source_environment
      pip install -r assets/requirements.txt
      pip install -r assets/requirements-dev.txt
      pip install pib_cli
    unvirtualize
  popd  > /dev/null
  echo "Pipenv Environment Location: $(pipenv --venv)"
}

source_environment() {

  if [[ ! -f /etc/container_release ]]; then

    unvirtualize

    # shellcheck disable=SC1090
    source "$(pipenv --venv)/bin/activate"

  fi

  pushd "${ROOT}"  > /dev/null
    set +e
      cd .git/hooks
      ln -sf ../../scripts/hooks/pre-commit pre-commit
    set -e
  popd  > /dev/null

}

spawn_shell() {
  if [[ "${ARG}" == "shell" ]]; then
    pushd "${ROOT}"  > /dev/null
      export PIB_CONFIG_FILE_LOCATION="./assets/cli.yml"
    popd  > /dev/null
    pipenv shell
  else
    echo "Run this script with the *shell* argument to spawn a shell within the virtual environment."
  fi
}

unvirtualize() {

  if [[ ! -f /etc/container_release ]]; then

    toggle=1

    if [[ -n "${-//[^e]/}" ]]; then set +e; else toggle=0; fi
      deactivate_present=$(LC_ALL=C type deactivate 2>/dev/null)
      if [[ -n ${deactivate_present} ]]; then
        deactivate
      fi
    if [[ "${toggle}" == "1" ]]; then set -e; fi

  fi

}

export PROJECT_NAME="pib_cli"
conditional_source
