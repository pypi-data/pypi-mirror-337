#! /usr/bin/env bash

function abcli_pypi() {
    local task=$1

    local options=$2
    local plugin_name=$(abcli_option "$options" plugin bluer_ai)

    local function_name=abcli_pypi_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    abcli_log_error "$plugin_name: pypi: $task: command not found."
    return 1
}

abcli_source_caller_suffix_path /pypi
