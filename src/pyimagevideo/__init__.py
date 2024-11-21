from __future__ import annotations
import numpy as np


def sixteen2eight(img, Clim: tuple[int, int]):
    """
    stretch uint16 data to uint8 data e.g. images

    Parameters
    ----------

    img: numpy.ndarray
        2-D Numpy array of grayscale image data
    Clim: tuple of int
        lowest and highest expected values

    """
    # stretch to [0,255] as a float
    Q = normframe(img, Clim) * 255

    return Q.astype(np.uint8)  # convert to uint8


def normframe(img, Clim: tuple[int, int]):
    """
    Normalize array to [0, 1]

    Parameters
    ----------

    img: numpy.ndarray
        data to be normalized
    Clim: tuple of int
        lowest and highest expected values
    """
    Vmin = Clim[0]
    Vmax = Clim[1]

    return (img.astype(np.float32).clip(Vmin, Vmax) - Vmin) / (Vmax - Vmin)


def wavelength2rgb(wavelength: float, gamma: float = 0.8) -> tuple[float, float, float]:
    """
    http://www.noah.org/wiki/Wavelength_to_RGB_in_Python

    This converts a given wavelength into an approximate RGB value.
    The given wavelength is in nanometers.
    The range of wavelength is 380 nm through 750 nm.

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    """

    wavelength = float(wavelength)
    if 440.0 >= wavelength >= 380.0:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    R = int(R * 255)
    G = int(G * 255)
    B = int(B * 255)

    assert 255 >= R >= 0 and 255 >= G >= 0 and 255 >= B >= 0

    return R, G, B


def tone(fs: int = 8000, T: float = 1, f0: float = 1000):
    """
    generate f0 Hz sinusoid for T seconds at fs S/s.
    """
    return np.sin(2 * np.pi * f0 * np.arange(0, T, 1 / fs))


def dialtone(fs: int = 8000, T: float = 1):
    """
    generate North American dial tone
    https://en.wikipedia.org/wiki/Precise_Tone_Plan
    """
    return 0.5 * (tone(fs, T, 440) + tone(fs, T, 350))
