#! /usr/bin/env bash

function abcli_storage() {
    local task=$1

    local function_name=abcli_storage_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    python3 -m bluer_objects.storage "$@"
}

abcli_source_caller_suffix_path /storage
