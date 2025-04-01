#! /usr/bin/env bash

function blue_south_action_git_before_push() {
    blue_south build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(bluer_ai_git get_branch)" != "main" ]] &&
        return 0

    blue_south pypi build
}
