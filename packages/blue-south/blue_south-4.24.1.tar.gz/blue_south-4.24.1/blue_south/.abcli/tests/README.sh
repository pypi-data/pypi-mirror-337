#! /usr/bin/env bash

function test_blue_south_README() {
    local options=$1

    abcli_eval ,$options \
        blue_south build_README
}
