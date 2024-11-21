#!/usr/bin/env python
"""
demo of measuring FPS performance with Matplotlib and OpenCV
i.e. how fast can I update an image plot

Example:
$ python FPS_matplotlib_image.py
matplotlib 3.0.2 imshow average FPS 27.66  over 100 frames.
matplotlib 3.0.2 pcolormesh average FPS 6.76  over 100 frames.
OpenCV 3.4.3 average FPS 226.59  over 100 frames.

Caveats:
1) I compiled OpenCV with OpenCL--it's possible imshow is using the GPU on my laptop (not sure if imshow uses the GPU)
2) This is an average measurement, so it doesn't capture bogdowns in the frame rate.
3) you must normalize your data on a [0,255] range for cv2.imshow

It's just a very simple comparison, showing OpenCV's huge FPS advantage

NOTE: we use pause(1e-3) as pause(1e-6) yields the same FPS, but doesn't give visible updates. A race condition in Matplotlib?

"""
from __future__ import annotations
import numpy as np
from numpy.random import rand
import matplotlib
from matplotlib.pyplot import figure, draw, pause, close
from time import time

try:
    import cv2
except ImportError:
    cv2 = None
#
Nfps = 100


def randomimg(xy: tuple[int, int]):
    """
    generate two image frames to toggle between
    """
    return (rand(2, xy[0], xy[1]) * 255).astype(np.uint8)


def fpsmatplotlib_imshow(dat):
    fg = figure()
    ax = fg.gca()
    h = ax.imshow(dat[0, ...])
    ax.set_title("imshow")
    tic = time()
    for i in range(Nfps):
        h.set_data(dat[i % 2, ...])
        draw(), pause(1e-3)
    close(fg)
    return Nfps / (time() - tic)


def fpsmatplotlib_pcolor(dat):
    fg = figure()
    ax = fg.gca()
    h = ax.pcolormesh(dat[0, ...])
    ax.set_title("pcolormesh")
    ax.autoscale(True, tight=True)
    tic = time()
    for i in range(Nfps):
        h.set_array(dat[i % 2, ...].ravel())
        draw(), pause(1e-3)
    close(fg)
    return Nfps / (time() - tic)


def fpsopencv(dat):
    tic = time()
    for i in range(Nfps):
        cv2.imshow("fpstest", dat[i % 2, ...])
        cv2.waitKey(1)  # integer milliseconds, 0 makes wait forever
    cv2.destroyAllWindows()
    return Nfps / (time() - tic)


if __name__ == "__main__":
    from argparse import ArgumentParser

    p = ArgumentParser(description="measure FPS for rapidly updating plot with Matplotlib vs. OpenCV")
    p.add_argument("-p", "--xypixels", help="number of pixels for x and y", type=int, default=(512, 512))
    P = p.parse_args()

    dat = randomimg(P.xypixels)

    fpsmat = fpsmatplotlib_imshow(dat)
    print(f"matplotlib {matplotlib.__version__} imshow average FPS {fpsmat:.2f}  over {Nfps} frames.")

    fpsmat = fpsmatplotlib_pcolor(dat)
    print(f"matplotlib {matplotlib.__version__} pcolormesh average FPS {fpsmat:.2f}  over {Nfps} frames.")

    if cv2:
        fpscv = fpsopencv(dat)
        print(f"OpenCV {cv2.__version__} average FPS {fpscv:.2f}  over {Nfps} frames.")
