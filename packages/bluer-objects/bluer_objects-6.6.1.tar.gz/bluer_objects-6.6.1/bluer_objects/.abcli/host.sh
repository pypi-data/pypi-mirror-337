#! /usr/bin/env bash

function abcli_host() {
    local task=$(abcli_unpack_keyword $1 void)
    local options=$2

    if [ $task == "get" ]; then
        python3 -m blue_options.host \
            get \
            --keyword "$2" \
            "${@:3}"
        return
    fi

    if [ $task == "reboot" ]; then
        abcli_eval ,$options \
            sudo reboot
        return
    fi

    if [ $task == "shutdown" ]; then
        abcli_eval ,$options \
            sudo shutdown -h now
        return
    fi

    abcli_log_error "@host: $task: command not found."
    return 1
}
