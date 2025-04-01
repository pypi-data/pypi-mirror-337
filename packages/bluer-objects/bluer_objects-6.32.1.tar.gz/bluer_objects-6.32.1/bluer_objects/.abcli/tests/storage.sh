#! /usr/bin/env bash

function test_bluer_objects_storage() {
    local options=$1

    local object_name=test_bluer_objects_storage-$(abcli_string_timestamp_short)
    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -pv $object_path

    local suffix
    local extension=yaml
    for suffix in this.$extension that.$extension subfolder/this.$extension subfolder/that.$extension; do
        python3 -m bluer_objects.file \
            create_a_file \
            --filename $object_path/$suffix
    done

    # testing upload
    abcli_hr

    bluer_objects_upload \
        filename=this.$extension \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_upload \
        filename=subfolder/this.$extension \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_upload \
        - \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    # clean-up
    rm -rfv $object_path
    abcli_hr

    # testing download

    bluer_objects_download \
        filename=this.$extension \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_download \
        filename=subfolder/this.$extension \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_download \
        - \
        $object_name
}
