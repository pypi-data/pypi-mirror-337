import pytest

from blueness import module

from bluer_objects import file, objects, NAME
from bluer_objects import storage

NAME = module.name(__file__, NAME)


@pytest.mark.parametrize(
    ["filename"],
    [["vancouver.geojson"]],
)
def test_objects_upload(
    filename: str,
):
    assert storage.download(object_name=VANWATCH_TEST_OBJECT)

    object_name = objects.unique_object("test_objects_upload_filename")

    source_filename = objects.path_of(
        filename=filename,
        object_name=VANWATCH_TEST_OBJECT,
    )
    destination_filename = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    assert file.copy(source_filename, destination_filename)

    assert objects.upload(object_name=object_name)

    assert file.delete(destination_filename)
    assert not file.exists(destination_filename)

    assert storage.download(object_name=object_name)

    assert file.exists(destination_filename)


@pytest.mark.parametrize(
    ["filename"],
    [["vancouver.geojson"]],
)
def test_objects_upload_filename(
    filename: str,
):
    assert storage.download(object_name=VANWATCH_TEST_OBJECT)

    object_name = objects.unique_object("test_objects_upload_filename")

    source_filename = objects.path_of(
        filename=filename,
        object_name=VANWATCH_TEST_OBJECT,
    )
    destination_filename = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    assert file.copy(source_filename, destination_filename)

    assert objects.upload(
        object_name=object_name,
        filename=filename,
    )

    assert file.delete(destination_filename)
    assert not file.exists(destination_filename)

    assert storage.download(
        object_name=object_name,
        filename=filename,
    )

    assert file.exists(destination_filename)
