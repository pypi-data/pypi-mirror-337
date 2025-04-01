#! /usr/bin/env bash

function test_bluer_ai_hr() {
    abcli_hr
}

function test_bluer_ai_log_local() {
    abcli_log_local "testing"
}

function test_bluer_ai_show_usage() {
    abcli_show_usage "command-line" \
        "usage"
}
