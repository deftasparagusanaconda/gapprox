def dft(values: list[complex]) -> list[complex]:
	"""discrete fourier transform"""

	from scipy.fft import fft
	return fft(values, norm="forward")
