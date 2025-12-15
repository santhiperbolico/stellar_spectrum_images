import argparse
import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

from utils import wavelength_to_rgb, read_fits

def get_params(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create spectrum from fits file")
    parser.add_argument("--object_name", type=str, help="Name of the object")
    parser.add_argument("--object_type", type=str, help="Type of the object.")
    parser.add_argument("--fits_file", type=str, help="Fits file name")
    return parser.parse_args(argv)


def create_spectrum(
        fits_file: str,
        object_name: str,
        object_type: str
) -> str:
    """
    Generates a spectrum visualization plot from a FITS file and saves it as a PNG image. The spectrum
    is normalized and shown within the visible light range (3800-7500 Å). The plot includes color-coded
    wavelength bands and a title based on the provided object name.

    Parameters
    ----------
    fits_file : str
        The path to the FITS file containing the light curve data.
    object_name : str
        The name of the object being visualized, used as the title of the spectrum plot.
    object_type : str
        The type or category of the object, displayed as a label on the spectrum plot.

    Returns
    -------
    str
        The file path of the saved PNG image containing the generated spectrum visualization.
    """
    df_light_curve = read_fits(fits_file)

    df_visible = df_light_curve[
        (df_light_curve['wavelength'] >= 3800) & (df_light_curve['wavelength'] <= 7500)
        ]

    wavelength = df_visible['wavelength'].values
    flux = df_visible['flux'].values
    norm_flux = flux / np.max(flux)
    norm_flux[norm_flux < 0] = 0

    n_bins = wavelength.size
    colors_wavelength = np.linspace(3800, 7500, n_bins)
    colors_rgb = np.array(
        [wavelength_to_rgb(w / 10) for w in colors_wavelength])

    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('xkcd:black')
    ax.set_facecolor('xkcd:black')

    for i in range(len(wavelength) - 1):
        color_index = int((wavelength[i] - 3800) / (7500 - 3800) * n_bins)
        color_index = np.clip(color_index, 0, n_bins - 1)
        color = colors_rgb[color_index]
        ax.fill_between([wavelength[i], wavelength[i + 1]], 0.15, 0.85, color=color,
                        transform=ax.get_xaxis_transform(), alpha=norm_flux[i])

    ax.plot(wavelength, norm_flux, color='black', linewidth=1.6)

    ax.set_xlim(3800, 7500)
    ax.set_ylim(-0.25, 1.35)
    ax.axis('off')
    fira_sans_2 = FontProperties(fname="fonts/Caveat-VariableFont_wght.ttf")

    fig.suptitle(object_name, color='white', size=20, font=fira_sans_2)
    fig.subplots_adjust(left=0.1)
    fig.text(0.02, 0.5, object_type, fontsize=30, color='white', va='center', ha='left',
             font=fira_sans_2)
    plt.tight_layout()
    plt.show()

    path = os.path.dirname(fits_file)
    output_file = os.path.join(path, f"{object_name}.png")
    fig.savefig(output_file)
    return output_file

def main(argv: list[str] | None = None):
    args = get_params(argv)
    object_name = args.object_name
    object_type = args.object_type
    fits_file = args.fits_file

    logging.info(f"-- Creating spectrum for {object_name}")
    output_file = create_spectrum(fits_file, object_name, object_type)
    logging.info(f"-- Saved spectrum to {output_file}")

if __name__ == "__main__":
    main(sys.argv[1:])
