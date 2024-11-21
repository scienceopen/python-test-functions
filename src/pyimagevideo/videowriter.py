import cv2
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def VideoWriter(fn: Path, cc4: str, xypix: tuple, fps: float, usecolor: bool):
    """

    Parameters
    ----------
    fn: pathlib.Path
        output filename to write
    cc4: str
        four character fourcc code e.g. 'FFV1'
    xypix: two-element tuple with x,y pixel count
    usecolor: bool color or bw
    """
    fn.parent.mkdir(parents=True, exist_ok=True)

    ncc4 = cv2.VideoWriter_fourcc(*cc4)

    hv = cv2.VideoWriter(str(fn), ncc4, fps=fps, frameSize=xypix, isColor=usecolor)

    if not hv or not hv.isOpened():
        raise RuntimeError(f"trouble starting video {fn}")

    yield hv

    hv.release()
