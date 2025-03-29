#! /usr/bin/env bash

function abadpour() {
    local task=$(abcli_unpack_keyword $1 version)

    abcli_generic_task \
        plugin=abadpour,task=$task \
        "${@:2}"
}

abcli_log $(abadpour version --show_icon 1)
