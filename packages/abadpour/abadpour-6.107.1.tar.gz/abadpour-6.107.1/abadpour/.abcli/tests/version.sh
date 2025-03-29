#! /usr/bin/env bash

function test_abadpour_version() {
    local options=$1

    abcli_eval ,$options \
        "abadpour version ${@:2}"

    return 0
}
