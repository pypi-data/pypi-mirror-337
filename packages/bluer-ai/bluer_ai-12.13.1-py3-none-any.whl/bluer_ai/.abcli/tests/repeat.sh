#! /usr/bin/env bash

function test_bluer_ai_repeat() {
    abcli_repeat - ls
    abcli_assert "$?" 0

    abcli_repeat count=3 ls
    abcli_assert "$?" 0
}
