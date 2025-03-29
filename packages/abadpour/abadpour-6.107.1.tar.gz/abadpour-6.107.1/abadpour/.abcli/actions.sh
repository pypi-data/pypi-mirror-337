#! /usr/bin/env bash

function abadpour_action_git_before_push() {
    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    abadpour pypi build

    abadpour build
}
