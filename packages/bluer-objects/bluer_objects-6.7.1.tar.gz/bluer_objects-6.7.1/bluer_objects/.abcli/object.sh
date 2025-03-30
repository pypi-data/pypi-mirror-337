#! /usr/bin/env bash

export ABCLI_S3_OBJECT_PREFIX=s3://$ABCLI_AWS_S3_BUCKET_NAME/$ABCLI_AWS_S3_PREFIX

function abcli_clarify_object() {
    local object_name=$1
    local default=${2:-$(abcli_string_timestamp)}
    local type_name=${3:-object}

    local object_var=abcli_${type_name}_name
    local object_var_prev=abcli_${type_name}_name_prev
    local object_var_prev2=abcli_${type_name}_name_prev2

    [[ -z "$object_name" ]] || [[ "$object_name" == "-" ]] &&
        object_name=$default

    if [ "$object_name" == "." ]; then
        object_name=${!object_var}
    elif [ "$object_name" == ".." ]; then
        object_name=${!object_var_prev}
    elif [ "$object_name" == "..." ]; then
        object_name=${!object_var_prev2}
    fi

    if [ "$(abcli_keyword_is $object_name validate)" == true ]; then
        local object_name="validate"
    fi

    mkdir -p $ABCLI_OBJECT_ROOT/$object_name

    echo $object_name
}

function abcli_object() {
    local task=$(abcli_unpack_keyword $1 void)

    if [ "$task" == "open" ]; then
        local object_name=$(abcli_clarify_object $2 .)

        abcli_download - $object_name

        rm -v ../$object_name.tar.gz
        aws s3 rm "$ABCLI_S3_OBJECT_PREFIX/$object_name.tar.gz"

        abcli_tags set $object_name ~solid

        abcli_upload - $object_name

        return
    fi

    abcli_log_error "@object: $task: command not found."
    return 1
}
