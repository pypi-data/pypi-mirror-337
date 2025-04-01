import pytest


from bluer_objects import file, objects
from bluer_objects import storage


@pytest.mark.parametrize(
    ["object_name", "filename"],
    [[VANWATCH_TEST_OBJECT, "vancouver.geojson"]],
)
def test_objects_download(
    object_name: str,
    filename: str,
):
    filename_fullpath = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    if file.exists(filename_fullpath):
        assert file.delete(filename_fullpath)

    assert not file.exists(filename_fullpath)

    assert objects.storage(object_name=object_name)

    assert file.exists(filename_fullpath)


@pytest.mark.parametrize(
    ["object_name", "filename"],
    [[VANWATCH_TEST_OBJECT, "vancouver.geojson"]],
)
def test_objects_download_filename(
    object_name: str,
    filename: str,
):
    filename_fullpath = objects.path_of(
        filename=filename,
        object_name=object_name,
    )
    if file.exists(filename_fullpath):
        assert file.delete(filename_fullpath)

    assert not file.exists(filename_fullpath)

    assert storage.download(
        object_name=object_name,
        filename=filename,
    )

    assert file.exists(filename_fullpath)
