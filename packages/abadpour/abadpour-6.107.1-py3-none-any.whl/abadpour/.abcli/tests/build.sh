#! /usr/bin/env bash

function test_abadpour_build() {
    local options=$1

    abcli_eval ,$options \
        "abadpour build \
        ${@:2}"
}
