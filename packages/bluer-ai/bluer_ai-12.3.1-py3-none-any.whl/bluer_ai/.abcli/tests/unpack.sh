#! /usr/bin/env bash

function test_abcli_unpack_repo_name() {
    abcli_assert \
        $(abcli_unpack_repo_name abcli) \
        awesome-bash-cli
}
