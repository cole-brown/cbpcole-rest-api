# Source this file.

_print_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "${_print_dir}/_debug.sh"


# ------------------------------------------------------------------------------
# Print Helpers
# ------------------------------------------------------------------------------

# Returns length of longest arg passed in.
LEN_MAX=0
max_len() {
    local _args=("$@")
    dbg_print "max_len of: ${_args[@]}"
    local _max=0
    local _len=0
    for arg in "${_args[@]}"; do
        # This is length of the current arg string.
        _len=${#arg}
        dbg_print "  $_len <-length- '${arg}'"
        if [ "$_len" -gt "$_max" ]; then
            dbg_print "  max update: $_len > $_max"
            _max=$_len
        fi
    done

    LEN_MAX=$_max
    dbg_print "max is $LEN_MAX"
}


# ------------------------------------------------------------------------------
# Print Functions
# ------------------------------------------------------------------------------

# Given character $1 (e.g. '─'), length $2 (e.g. 10), and string $3 (e.g. '\n' or ''),
# builds a string of $1 characters of length $2, ending with $3.
# String is in variable $LINE_BUILT
#
# Args:
#   required:
#     $1 - (int) length
#   optional:
#     $2 - char to use for line ('─' if no $2)
#     $3 - append a newline if $3 exists.
#
# Examples:
#   build_line 10 '─' '\n'
#   build_line 10 '─' 1
#     "──────────\n"
#   build_line 10 '─'
#     "──────────"
LINE_BUILT=''
build_line () {
    dbg_print "<build_line>"

    LINE_BUILT=''

    local _length=$1

    # Character to use for line or default.
    local _char="$2"
    if [ -z $_char ]; then
        _char='─'
    fi

    # Should we append a newline?
    local _end=''
    if [ ! -z "$3" ]; then
        _end='\n'
    fi

    # Build the line into the public var.
    dbg_print "_length: $_length"
    dbg_print "_char:   '$_char'"
    dbg_print "   \$2: '$2'"
    dbg_print "_end:    '$_end'"

    LINE_BUILT=$(printf "%0*d" $_length 0 | sed "s/0/$_char/g")
    LINE_BUILT="${LINE_BUILT}${_end}"

    dbg_print "LINE_BUILT: '$LINE_BUILT'"
    dbg_print "</build_line>"
}


# Given character $1 (e.g. '─'), length $2 (e.g. 10), and string $3 (e.g. '\n' or ''),
# print out a string of $1 characters of length $2, ending with $3.
#
# Args:
#   required:
#     $1 - (int) lengt
#   optional:
#     $2 - char to use for line ('─' if no $2)
#     $3 - append a newline if $3 exists.
#
# Examples:
#   print_line '─' 10 '\n'
#   print_line '─' 10 1
#     "──────────\n"
#   print_line '─' 10
#     "──────────"
print_line () {
    dbg_print "<print_line args=$@>"
    local _length=$1

    # Character to use for line or default.
    local _char="$2"
    if [ -z $_char ]; then
        _char='─'
    fi

    # Should we append a newline?
    local _end=''
    if [ -z "$3" ]; then
        _end='\n'
    fi

    # Build and print the line.
    dbg_print "_length: $_length"
    dbg_print "_char:   '$_char'"
    dbg_print "_end:    '$_end'"

    printf "%0*d" $_length 0 | sed "s/0/$_char/g"
    if [ ! -z $_end ]; then
        printf $_end
    fi
    dbg_print "</print_line>"
}


# Prints:
#   $1 + (left aligned, space padded $2) + $4[\n if $5]
# Args:
#   - $1 - prefix
#   - $2 - line contents
#   - $3 - line width
#   - $4 - postfix
#   - $5 - include newlin?
print_enclosed () {
    dbg_print "<print_enclosed>"
    dbg_print "  @args:"
    for arg in "${_args[@]}"; do
        "  - '$arg'"
    done

    # ------------------------------
    # Parse inputs.
    # ------------------------------
    local _newline=''
    local _align=''
    local OPTIND OPTARG arg
    while getopts ":na:" arg; do
        dbg_print "getopts arg: '$arg'"
        case $arg in
            n)
                dbg_print "  :newline"
                _newline='true'
                ;;
            a)
                dbg_print "  :align $OPTARG"
                case $OPTARG in
                    l|left)
                        _align='left'
                        dbg_print "    left: '$_align'"
                        ;;
                    r|right)
                        _align='right'
                        dbg_print "    right: '$_align'"
                        ;;
                    *)
                        echo "Unknown alignment arg: '$OPTARG'. Use 'l', 'left', 'r', or 'right'."
                        dbg_print "</print_enclosed>"
                        return 1
                esac
                ;;
            *)
                echo "Failed parsing args."
                echo "  unknown arg: '$OPTARG'"
                dbg_print "</print_enclosed>"
                return 1
        esac
    done
    shift $((OPTIND-1))

    local _prefix=$1
    local _line=$2
    local _line_width=$3
    local _postfix=$4

    dbg_print "print_enclosed():"
    dbg_print "  _prefix:  '$_prefix'"
    dbg_print "  _line:    '$_line'"
    dbg_print "    _align: $_align"
    dbg_print "    _width: $_line_width"
    dbg_print "  _postfix: '$_postfix'"
    if [ -z "$_newline" ]; then
        dbg_print "  _newline: false"
    else
        dbg_print "  _newline: $_newline"
    fi

    # ------------------------------
    # Sanity Check Inputs.
    # ------------------------------

    local _fail=''
    if [ -z "$_prefix" ]; then
        echo "print_enclosed: prefix is require to exist: '$_prefix'"
        fail=1
    fi
    if [ -z "$_line" ]; then
        echo "print_enclosed: line is require to exist: '$_line'"
        fail=1
    fi
    if [ -z "$_line_width" ]; then
        echo "print_enclosed: line_width is require to exist: '$_line_width'"
        fail=1
    fi
    if [ -z "$_postfix" ]; then
        echo "print_enclosed: postfix is require to exist: '$_postfix'"
        fail=1
    fi
    if [ ! -z "$_fail" ]; then
        dbg_print "</print_enclosed exit=1>"
        return 1
    fi

    # ------------------------------
    # Actual print.
    # ------------------------------

    # Print it out with \n or not.
    printf "%s" $_prefix

    if [ -z "$align" ] -o [ "$align" == "right" ]; then
        printf "%s%${_line_width}" $_line
    else  # left align
        printf "%s%${_line_width}" $_line
    fi

    printf "%s" $_postfix

    if [ ! -z "$_newline" ]; then
        printf "\n"
    fi

    dbg_print "</print_enclosed>"
}


_et_length=0
# Trim whitespace from $1, echo it, and store its length in `_et_length`.
echo_trim () {
    dbg_print "<echo_trim>"
    _et_length=0
    dbg_print "trimming..."
    # Use xargs to trim whitespace
    local _output=$(printf "%s" "$1" | xargs)
    # echo trimmed, return length of output.
    dbg_print "trimmed"
    dbg_print "trimmed input is: '$1'"
    dbg_print "trimmed output is: '$_output'"
    _et_length=${#_output}
    dbg_print "trimmed len $_et_length"
    echo "$_output"
    dbg_print "</echo_trim>"

    return 0
}

