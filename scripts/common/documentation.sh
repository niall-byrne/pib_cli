#!/usr/bin/env bash
# shellcheck disable=SC1117

build_documentation() {

  echo "Generating Documentation ..."
  set -e

  pushd "${PROJECT_HOME}/documentation" > /dev/null
    rm -rf build
    make html
  popd > /dev/null

}
