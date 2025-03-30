#! /usr/bin/env bash

function blue_south() {
    local task=$(abcli_unpack_keyword $1 version)

    abcli_generic_task \
        plugin=blue_south,task=$task \
        "${@:2}"
}

abcli_log $(blue_south version --show_icon 1)
