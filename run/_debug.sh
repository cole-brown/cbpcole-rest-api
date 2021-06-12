#!/usr/bin/env bash

#-------------------------------------------------------------------------------
# Debug Helper
#-------------------------------------------------------------------------------

# Enable/disable dbg_print() output.
_dbg_print_mode=''  # 'yes' # ''

dbg_print() {
    if [ -z "$_dbg_print_mode" ]; then
        return 0
    fi

    echo "$@"
    return 0
}

