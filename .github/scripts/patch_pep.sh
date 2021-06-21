#!/bin/bash

set -eo pipefail

main() {

  git apply patches/pep.patch
  dev reinstall-requirements
  black --check .
  dev fmt
  dev lint

}

main "$@"
