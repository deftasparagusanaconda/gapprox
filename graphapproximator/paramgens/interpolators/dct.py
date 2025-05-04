def dct(values, dct_type = 2):
	"""discrete cosine transform
	dct_type: 1, 2, 3, 4"""

	from scipy.fft import dct

	if dct_type in [5,6,7,8]:
		raise ValueError(f"dct_type {dct_type} is not yet implemented")
	elif dct_type not in [1,2,3,4]:
		raise ValueError("dct() got invalid dct_type")

	return dct(values, type=dct_type, norm="forward")

