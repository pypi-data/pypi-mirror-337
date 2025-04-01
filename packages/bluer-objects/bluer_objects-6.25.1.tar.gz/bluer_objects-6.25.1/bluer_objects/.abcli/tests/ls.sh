#! /usr/bin/env bash

function test_bluer_objects_ls() {
    bluer_ai_select

    abcli_upload

    bluer_ai_ls cloud

    bluer_ai_ls local

    bluer_ai_ls "$abcli_path_bash/tests/*.sh"
}
