#! /usr/bin/env bash

function blue_south() {
    local task=$1

    abcli_generic_task \
        plugin=blue_south,task=$task \
        "${@:2}"
}

abcli_log $(blue_south version --show_icon 1)
