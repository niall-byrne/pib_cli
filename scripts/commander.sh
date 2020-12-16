#!/bin/bash

set -e

# shellcheck source=scripts/common/common.sh
source "$( dirname "${BASH_SOURCE[0]}" )/common/common.sh"

# shellcheck source=scripts/settings.sh
source "$( dirname "${BASH_SOURCE[0]}" )/settings.sh"

# shellcheck source=scripts/common/documentation.sh
source "$( dirname "${BASH_SOURCE[0]}" )/common/documentation.sh"

# Optional For Libraries
# shellcheck source=scripts/common/wheel.sh
# source "$( dirname "${BASH_SOURCE[0]}" )/common/wheel.sh"

# Add Additional Functionality Via Imports Here

case $1 in
  'build-docs')
    shift
    source_environment
    build_documentation "$@"
    ;;
  'lint')
    shift
    source_environment
    lint "$@"
    ;;
  'lint-validate')
    shift
    source_environment
    lint_check "$@"
    ;;
  'reinstall-requirements')
    shift
    source_environment
    reinstall_requirements "$@"
    ;;
  'sectest')
    shift
    source_environment
    security "$@"
    ;;
  'setup')
    shift
    setup_bash "$@"
    setup_python "$@"
    ;;
  'shortlist')
    echo "build-docs lint lint-validate reinstall-requirements sectest setup test test-coverage update"
    ;;
  'test')
    shift
    source_environment
    unittests "$@"
    ;;
  'test-coverage')
    shift
    source_environment
    unittests "coverage" "$@"
    ;;
  'update')
    shift
    update_cli "$@"
    ;;
  *)
    echo "Valid Commands:"
    echo ' - build-docs              (Build Documentation)'
    echo ' - lint                    (Run the linter)'
    echo ' - lint-validate           (Validate linting)'
    echo ' - reinstall-requirements  (Reinstall Packages'
    echo ' - sectest                 (Run security tests)'
    echo ' - setup                   (Setup/Reset environment)'
    echo ' - test                    (Run pytest)'
    echo ' - test-coverage           (Run pytest with coverage)'
    echo ' - update                  (Update bash & the CLI)'
    ;;

esac
