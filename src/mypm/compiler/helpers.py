def _generate_helpers() -> str:
    return """\
# fwrapper <command> [args...]
#
# Runs a command with output controlled by fwrapper_log_level.
# Arguments prefixed with "--fwrapper_" are reserved for fwrapper itself
# and are not passed to the command.
#
# --fwrapper_log_level=debug   show all output (stdout + stderr)
# --fwrapper_log_level=info    show stdout only, suppress stderr
# --fwrapper_log_level=silent  suppress all output (default)
# --fwrapper_log_level=null    suppress all output
#
# Example:
#   fwrapper ls -la
#   fwrapper --fwrapper_log_level=info ls -la
_resolve_log_level() {
    local log_level="$1"
    shift
    case "$log_level" in
        debug) "$@" ;;
        info)  "$@" 2>/dev/null ;;
        *)     "$@" > /dev/null 2>&1 ;;
    esac
}

fwrapper() {
    local original_dir="$PWD"
    local cmd_args=()
    local log_level="silent"
    for arg in "$@"; do
        if [[ "$arg" == --fwrapper_* ]]; then
            case "$arg" in
                --fwrapper_log_level=*) log_level="${arg#--fwrapper_log_level=}" ;;
            esac
        else
            cmd_args+=("$arg")
        fi
    done
    _resolve_log_level "$log_level" "${cmd_args[@]}"
    cd "$original_dir"
}
"""


def generate_helpers() -> str:
    return _generate_helpers()
