def dst(values, dst_type = 2):
	"""discrete sine transform
	dst_type: 1, 2, 3, 4"""

	from scipy.fft import dst

	if dst_type in [5,6,7,8]:
		raise ValueError(f"dst_type {dst_type} is not yet implemented")
	elif dst_type not in [1,2,3,4]:
		raise ValueError("dst() got invalid dst_type")

	return dst(values, type=dst_type, norm="forward")

