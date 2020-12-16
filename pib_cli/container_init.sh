#!/bin/bash

DEVELOPMENT() {
  pushd "pib_cli" || exit 127
  while true; do sleep 1; done
}

PRODUCTION() {
  pushd "pib_cli" || exit 127
  while true; do sleep 1; done
}

eval "${ENVIRONMENT}"
