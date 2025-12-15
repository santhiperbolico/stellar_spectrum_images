from create_spectrum import create_spectrum

if __name__ == "__main__":
    fits_file = "examples/castor_spectrum.fits"
    create_spectrum(fits_file, "Castor", "A1")