#!/usr/bin/env python3
"""
Note:

* imageio.mimwrite expects dimensions (x,y,3)
* VLC has a long-standing bug where files under about 3fps don't playback

"""
import subprocess
import numpy as np
import tempfile
import imageio.v3 as iio
import shutil

EXE = shutil.which("ffplay")  # path to your video player
if not EXE:
    raise FileNotFoundError("FFplay was not found")

usecolor = False
nframe = 90
xpix = ypix = 256

ext = ".avi"
fps = 10

# %% generate noise signal
shape = (nframe, ypix, xpix, 3) if usecolor else (nframe, ypix, xpix)

vid = (np.random.random(shape) * 255).astype(np.uint8)
# %% write lossless AVI
with tempfile.NamedTemporaryFile(suffix=ext) as f:
    fn = f.name
    iio.imwrite(fn, vid)
    # %% check video
    subprocess.check_call([EXE, fn])
