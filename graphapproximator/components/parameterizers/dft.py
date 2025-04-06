from scipy.fft import fft

def dft(values: list[complex]) -> list[complex]:
        """discrete fourier transform"""

        return fft(values, norm="forward")
