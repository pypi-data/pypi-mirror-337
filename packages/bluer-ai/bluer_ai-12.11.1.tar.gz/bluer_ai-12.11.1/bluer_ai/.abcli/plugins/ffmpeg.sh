#! /usr/bin/env bash

function abcli_ffmpeg() {
    local task=$1

    local function_name=abcli_ffmpeg_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    abcli_log_error "@ffmpeg: $task: command not found."
    return 1
}

abcli_source_caller_suffix_path /ffmpeg
