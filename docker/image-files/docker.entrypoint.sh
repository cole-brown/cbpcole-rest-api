#!/usr/bin/env bash

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

source "${_test_dir}/_debug.sh"
source "${_test_dir}/_print.sh"


#-------------------------------------------------------------------------------
# set options:
#-------------------------------------------------------------------------------
# Set these after imports so they don't get accidentally wiped.
#
#   -e:          exit on first non-zero exit/return code
#   -u:          do not allow unset variables (error on them)
#                  - Don't set this; want to be more permissible in the entrypoint.
#   -o pipefail: if a command in a pipe chain exits non-zero, fail whole chain
#                with that exit code
set -euo pipefail



# ------------------------------------------------------------------------------
# Constants & Variables
# ------------------------------------------------------------------------------

host='0.0.0.0' # 'localhost' # 127.0.0.1
port=8080


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

title_unnecessarily_pretty() {
    local _title="$1"
    local _subtitle="$2"

    if [ -z "$_title" ]; then
        _title="UNKNOWN"
    fi

    if [ -z "$_subtitle" ]; then
        max_len "$_title"
        LEN_MAX=$((LEN_MAX + 10))
    else
        max_len "$_subtitle"
    fi
    local _width=$LEN_MAX

    if ! build_line $_width '─' ''; then
        echo "version_print: build_line('─') failed?!"
        echo "  build_line $_width '─' '\n'"
        echo "    -> LINE_BUILT: '$LINE_BUILT'"
    fi
    local _solid_line="$LINE_BUILT"

    # ...cuz I'm a sucker for centered titles. >.<
    local _padding=''
    local _left=''
    local _right=''
    (( _padding=($_width - ${#_title}) ))
    (( _left=($_padding / 2) )) # floor
    (( _right=(($_padding + 2 - 1) / 2) )) # ceiling

    dbg_print "width: $_width"
    dbg_print "title: ${#_title}"
    dbg_print "padding: $_padding"
    dbg_print "left: $_left"
    dbg_print "right: $_right"

    # ------------------------------
    # Print out a super-ultra-mega-pretty versions info box.
    # ------------------------------

    printf "    ┌─%s─┐\n" "$_solid_line"
    printf "    │ %${_left}s%s%${_right}s │\n" '' "$_title" ''
    printf "    │ %s │\n" "$_subtitle"
    printf "    └─%s─┘\n" "$_solid_line"

    echo
}


run_pip_install() {
    pushd "$CODE_ROOT_DIR" >/dev/null
    # We mount the code volume, so pip install it now.
    pip install --no-cache-dir -e .
    popd >/dev/null
}


run_server() {
    pushd $CODE_ROOT_DIR >/dev/null

    # ------------------------------
    # Just comment out if not desired:
    # ------------------------------
    local _title="cole"
    local _subtitle="(CBPC of Logging End-users)"
    title_unnecessarily_pretty "$_title" "$_subtitle"

    # ------------------------------
    # Get Host/Port
    # ------------------------------
    local _host="${1-${host}}"
    local _port="${2-${port}}"
    echo "  host: $_host"
    echo "  port: $_port"

    # ------------------------------
    # Run backend.
    # ------------------------------
    # Take over pid 1.
    #
    # Python Script:
    # exec /usr/bin/env python3 "cole/main.py" \
    #     --host $_host \
    #     --port $_port
    #
    # Flask expect some of these to be set in the environment:
    #  - FLASK_APP
    #  - FLASK_ENV
    exec /usr/bin/env python3 \
        -m flask run \
        --host $_host \
        --port $_port

    popd >/dev/null
}


run_tester() {
    pushd $CODE_ROOT_DIR >/dev/null

    # ------------------------------
    # Just comment out if not desired:
    # ------------------------------
    local _title="test"
    local _subtitle='Test `cole` functionality against reqs.'
    title_unnecessarily_pretty "$_title" "$_subtitle"

    # ------------------------------
    # Run tests.
    # ------------------------------
    /usr/bin/env python3 "test/main.py"

    popd >/dev/null
}

#-------------------------------------------------------------------------------
# Script
#-------------------------------------------------------------------------------

# Install our source.
run_pip_install

# # Is this our docker ip?
# ip_addr=$(ip route get 1.1.1.1 | awk '/via/{print $3}')
# echo
# echo "Docker IP: $ip_addr"
# # Default to hosting on the Docker network IP.
# if [ ! -z "$ip_addr" ]; then
#     host="$ip_addr"
# fi
# Flask didn't like that. I guess just 0.0.0.0.

# Switch to code's dir since we almost always want to be there.
cd "$CODE_ROOT_DIR"

# Run whatever user called. Do it this way instead of 'exec "$@"' as we can
# call functions this way.
echo
TARGET="$1"
shift
"$TARGET" "$@"
