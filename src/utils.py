import pandas as pd
from astropy.io import fits

def wavelength_to_rgb(wavelength: float, gamma=0.8) -> tuple[float, float, float, float]:
    """
    Convert a wavelength of light to an approximate RGB color.

    Taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This function takes a wavelength of light, expressed in nanometers, and
    converts it into an approximate RGB representation. The conversion is
    based on physical principles of light and human color perception. The
    function also applies gamma correction to the resulting RGB values to
    compensate for non-linear human visual perception.

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range

    Parameters
    ----------
    wavelength : float
        The wavelength of light in nanometers. Valid range is approximately
        380 nm to 750 nm.
    gamma : float, optional
        The gamma correction factor to be applied to the resulting RGB
        values. Default is 0.8.

    Returns
    -------
    R: float
        Red intensity, normalized between 0.0 and 1.0.
    G: float
        Green intensity, normalized between 0.0 and 1.0.
    B: float
        Blue intensity, normalized between 0.0 and 1.0.
    A: float
        Alpha (opacity), normalized between 0.0 and 1.0.

    Notes
    -----
    - Wavelength values outside the range of visible light (380-750 nm)
      are clamped to the nearest visible values.
    - The alpha (opacity) is set to 1.0 for visible wavelengths and
      0.5 for non-visible wavelengths.
    - The calculation of RGB values is based on approximations and may
      not perfectly match actual physical or perceptual characteristics
      of light for specific wavelengths.
    """

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A=0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength >750:
        wavelength = 750.
    if wavelength >= 380 and wavelength <= 440:
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
    return (R,G,B,A)


def read_fits(fits_file: str) -> pd.DataFrame:
    """
    Reads data from a FITS file and converts it into a Pandas DataFrame format.

    This function opens the specified FITS file, extracts data from the first HDU
    (Header/Data Unit), and structures specific fields such as flux, wavelength,
    inverse variance (ivar), normalization, bitwise AND mask, and bitwise OR mask
    into a DataFrame. The returned DataFrame contains these fields with their
    respective float representations.

    Parameters
    ----------
    fits_file : str
        The path to the FITS file to be read.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the extracted data with the following columns:
        flux, wavelength, ivar, normalization, andmask, ormask.
    """
    hdul = fits.open(fits_file)
    data = hdul[1].data
    df_light_curve = pd.DataFrame({
        "flux": data["FLUX"][0].astype(float),
        "wavelength": data["WAVELENGTH"][0].astype(float),
        "ivar": data["IVAR"][0].astype(float),
        "normalization": data["NORMALIZATION"][0].astype(float),
        "andmask": data["ANDMASK"][0].astype(float),
        "ormask": data["ORMASK"][0].astype(float),
    })
    return df_light_curve
