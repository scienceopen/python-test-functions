#!/usr/bin/env python
import pytest
from pathlib import Path

R = Path(__file__).parents[1]


def test_cv2codec_read():
    cv2 = pytest.importorskip("cv2")

    fn = R / "tests/star_collapse_out.avi"
    vid = cv2.VideoCapture(str(fn))

    ret, img = vid.read()  # a 3-D Numpy array, last axis is BGR: blue,green,red
    vid.release()

    assert ret, "could not open video"
    assert img.shape == (480, 720, 3), "video not decoded properly"

    cv2.imshow(f"OpenCV {cv2.__version__} {fn.name}", img)
    cv2.waitKey(delay=1000)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    pytest.main(["-x", __file__])
