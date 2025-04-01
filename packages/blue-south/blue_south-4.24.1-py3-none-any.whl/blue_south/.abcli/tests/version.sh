#! /usr/bin/env bash

function test_blue_south_version() {
    local options=$1

    abcli_eval ,$options \
        "blue_south version ${@:2}"
}
