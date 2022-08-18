#!/bin/bash

# scripts/utilities/reformat_file.sh
# Run code formatters inside the container, on a specific file.  (For IDE integration.)

# Host machine only:  Please do not use this script inside a PIB container.

main() {

  docker-compose run -T pib_cli dev fmt "$1"

}

main "$@"

