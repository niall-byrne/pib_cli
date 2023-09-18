#!/bin/bash

# scripts/utilities/install_gitleaks.sh
# Install a specific version of the gitleaks binary.

# This script can be used in any generic x64 Linux environment.

set -eo pipefail

TARGET_ARCH="amd64"

main() {

    curl --fail -sL "https://github.com/pelletier/go-toml/releases/download/${VERSION_TOMLL}/tomll_linux_${TARGET_ARCH}.tar.xz" -o tomll.tar.xz
    tar xvf tomll.tar.xz
    mv tomll /usr/bin
    chmod +x /usr/bin/tomll

}

main
