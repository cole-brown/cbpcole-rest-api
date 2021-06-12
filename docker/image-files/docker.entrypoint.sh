#!/usr/bin/env bash

# set options:
#   -e:          exit on first non-zero exit/return code
#   -u:          do not allow unset variables (error on them)
#                  - Don't set this; want to be more permissible in the entrypoint.
#   -o pipefail: if a command in a pipe chain exits non-zero, fail whole chain
#                with that exit code
set -euo pipefail


#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

# None.


#-------------------------------------------------------------------------------
# Script
#-------------------------------------------------------------------------------

# Switch to code's dir since we almost always want to be there.
cd "$CODE_ROOT_DIR"

# Run whatever user called. Do it this way instead of 'exec "$@"' as we can
# call functions this way.
TARGET="$1"
shift
"$TARGET" "$@"
