from __future__ import annotations
from pathlib import Path

import imageio.v3 as iio
from skimage.transform import resize
import numpy as np


def png2tiff(ofn: Path, pat: str, indir: Path | None = None):
    """
    convert series of PNG, which may not be exactly the same shape,
    to a multipage TIFF (in the same directory)

    alternatives: use ImageMagick from command line, or Wand.
    however, since the files are grouped in a specific weird way, the histfeas program
    worked best to have this perhaps ImageMagick duplicative functionality in
    Python/imageio/skimage.
    """

    ofn = Path(ofn).expanduser()
    indir = ofn.parent if indir is None else Path(indir).expanduser()
    # %% convert these sets of images to multipage image
    flist = sorted(indir.glob(pat))  # yes, sorted()
    if not flist:
        raise FileNotFoundError("found no files with {pat} in {ofn}")

    im0 = iio.imread(flist[0])  # priming read
    images = np.empty((len(flist), *im0.shape), dtype=im0.dtype)
    for i, f in enumerate(flist):
        im = iio.imread(f)
        images[i, ...] = resize(im, im0.shape, mode="edge")  # they are all of slightly different shape

    iio.imwrite(ofn, images)
