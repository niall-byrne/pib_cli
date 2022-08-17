#!/bin/bash

# scripts/utilities/install_gitleaks.sh
# Install a specific version of the gitleaks binary.

# This script can be used in any generic x64 Linux environment.

set -eo pipefail

TARGET_ARCH="x64"

main() {

  curl --fail -sL                                                                                                                                \
    "https://github.com/zricethezav/gitleaks/releases/download/v${VERSION_GITLEAKS}/gitleaks_${VERSION_GITLEAKS}_linux_${TARGET_ARCH}.tar.gz"    \
    -o gitleaks.tar.gz                                                                                                                        && \
    tar -xvzf gitleaks.tar.gz gitleaks                                                                                                        && \
    mv ./gitleaks /usr/bin/gitleaks                                                                                                           && \
    rm gitleaks.tar.gz                                                                                                                        && \
    chmod +x /usr/bin/gitleaks

}

main
