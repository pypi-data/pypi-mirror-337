#! /usr/bin/env bash

function abcli_mlflow_cache() {
    local task=$1

    local keyword=$2

    if [ "$task" == "read" ]; then

        abcli_mlflow_tags get \
            $keyword \
            --tag referent \
            "${@:3}"

        return
    fi

    if [ "$task" == "write" ]; then
        local value=$3

        abcli_mlflow_tags set \
            $keyword \
            referent=$value \
            "${@:4}"

        return
    fi

    abcli_log_error "@mlflow: cache: $task: command not found."
    return 1
}
