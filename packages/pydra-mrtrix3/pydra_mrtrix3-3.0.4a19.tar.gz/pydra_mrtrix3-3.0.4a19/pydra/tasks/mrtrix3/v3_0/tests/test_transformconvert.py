# Auto-generated test for transformconvert

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import TransformConvert


def test_transformconvert(tmp_path, cli_parse_only):

    task = TransformConvert(
        debug=False,
        force=False,
        input=[File.sample()],
        operation="flirt_import",
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
