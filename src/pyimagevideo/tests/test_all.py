#!/usr/bin/env python
import tempfile
import pytest
from pathlib import Path
import imageio

#
import pyimagevideo as piv
import pyimagevideo.gen_image as pimg

R = Path(__file__).parents[1]


def test_tiff_multipage_rw():
    pytest.importorskip("skimage")
    pytest.importorskip("matplotlib")

    with tempfile.TemporaryDirectory() as d:
        d = Path(d).expanduser()

        pimg.genimgseries(d)

        ofn = d / "mp.tif"
        piv.png2tiff(ofn, "[0-9].png")

        y = imageio.mimread(ofn)

    assert len(y) == 10


def test_wavelength2rgb():
    assert piv.wavelength2rgb(720) == (146, 0, 0)


if __name__ == "__main__":
    pytest.main(["-x", __file__])
