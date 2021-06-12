#!/usr/bin/env bash

# set options:
#   -e:          exit on first non-zero exit/return code
#   -u:          do not allow unset variables (error on them)
#                  - Don't set this; want to be more permissible in the entrypoint.
#   -o pipefail: if a command in a pipe chain exits non-zero, fail whole chain
#                with that exit code
set -euo pipefail

# Get our parent dir so we can figure out stuff is.
_build_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Constants & Variables
# ------------------------------------------------------------------------------

# ------------------------------
# Name & Version
# ------------------------------
_server_name='cole-clostra-homework-server'
_tester_name='cole-clostra-homework-test'
_version='latest'


# ------------------------------------------------------------------------------
# Hello There.
# ------------------------------------------------------------------------------

echo "────────────────────────────────────────────────────────────────────────────────"
echo "Build '$_version' Docker containers for:"
echo "  - $_server_name"
echo "  - $_tester_name"
echo "────────────────────────────────────────────────────────────────────────────────"


# ------------------------------------------------------------------------------
# Indent Function
# ------------------------------------------------------------------------------

indent() { sed 's/^/  /'; }


# ------------------------------------------------------------------------------
# Set-Up
# ------------------------------------------------------------------------------

# Down one and into the code.
_code_dir="${_build_dir}/../code"


# ------------------------------
# pushd now & popd on exit
# ------------------------------
pushd $_build_dir >/dev/null 2>&1

trap -- 'popd >/dev/null 2>&1; exit' EXIT
trap -- 'popd >/dev/null 2>&1; exit' SIGHUP
trap -- 'popd >/dev/null 2>&1; exit' SIGINT
trap -- 'popd >/dev/null 2>&1; exit' SIGQUIT
trap -- 'popd >/dev/null 2>&1; exit' SIGTERM


# ------------------------------------------------------------------------------
# Build Function
# ------------------------------------------------------------------------------

build_container() {
    local _container="$1"
    local _version="$2"

    # Error check params.
    if [ -z "$_container" ]; then
        echo "'build_container' requires the container name as argument \$1"
    fi
    if [ -z "$_version" ]; then
        echo "'build_container' requires the version name as argument \$2"
    fi

    # Shift off container/version - rest will be passed to docker.
    shift 2

    # Building with the currend dir (hopefully teh code folder) as context.
    _build_context_dir=$PWD

    # Print start message.
    echo
    echo "  ────────────────────────────────────────────────────────"
    echo "  Building '$_container' Docker images..."
    echo "  ────────────────────────────────────────────────────────"
    echo "    context: ${_build_context_dir}"
    echo "    extra input args: $@"
    echo
    echo "    docker build \\"
    echo "      -t ${_container}:latest \\"
    echo "      -t ${_container}:${_version} \\"
    echo "      -f build-files/build.docker.txt \\"
    echo "      $@ \\"
    echo "      ${_build_context_dir}"
    echo "  ────────────────────────────────────────────────────────"
    echo

    # Do the actual build.
    docker build -t ${_container}:latest -t ${_container}:${_version} -f build-files/build.docker.txt $@ ${_build_context_dir} # | indent
    echo
    echo "  Done."
    echo "  ────────────────────────────────────────────────────────"
}

# ------------------------------------------------------------------------------
# Build both containers.
# ------------------------------------------------------------------------------

build_container $_server_name $_version $@
build_container $_tester_name $_version $@


# ------------------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------------------

echo
echo "────────────────────────────────────────────────────────────────────────────────"
echo "Builds completed."
echo "────────────────────────────────────────────────────────────────────────────────"
