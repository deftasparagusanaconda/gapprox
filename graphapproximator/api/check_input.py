from utils import Colours, short_repr, MAX_PRINTED_ARRAY_DIM

def warn_input_1D(data):
	"""warns if the input is a 1D array
the expected format is two arrays: ([x1, x2, x3, ...], [y1, y2, y3, ...])
recommends x array as range(len(data)) if the elements of input are not iterable"""
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes at least [x1, x2, x3, ...], [y1, y2, y3, ...]")
	print(f"did you mean\t: {short_repr(range(min(MAX_PRINTED_ARRAY_DIM+1,len(data))))}, {short_repr(data)}")
	print(f"if yes, try\t: ga.input = ga._assume_x_array(ga.input)")
	print()
	return True

def warn_input_more_than_2D(data):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes (input arrays), (output arrays)")
	print(f"did you mean\t: {short_repr(_assume_first_one_input(data))}")
	print(f"if yes, try\t: ga.input = ga._assume_first_one_input(ga.input)")
	print(f"did you mean\t: {short_repr(_assume_last_one_output(data))}")
	print(f"if yes, try\t: ga.input = ga._assume_last_one_output(ga.input)")
	print()
	return True

def warn_input_shape(data):
	"""warns if the input is likely a list of coordinate pairs, e.g., (x1, y1), (x2, y2), (x3, y3), ...
the expected format is an array of value arrays: [x1, x2, x3, ...], [y1, y2, y3, ...], ...
recommends transpose() if the number of rows >= the number of columns"""
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes [x1, x2, x3, ...], [y1, y2, y3, ...], ...")

	try:
		transposed = list(zip(*data))
		pieces = [short_repr(row) for row in transposed]

		if len(pieces) > MAX_PRINTED_ARRAY_DIM:
			print(f"did you mean\t: {', '.join(pieces[:MAX_PRINTED_ARRAY_DIM])}, ...")
		else:
			print(f"did you mean\t: {', '.join(pieces)}")

	except Exception:
		print(f"did you mean\t: (couldnt auto-suggest fix, sowwyy)")
	
	print(f"if yes, try\t: ga.input = ga._transpose(ga.input)")
	print()
	return True

def warn_input_ragged_matrix(i,j,k):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: found inconsistent array lengths")
	print("suggestion\t: pad with zeroes to longest array")
	print("if yes, try\t: ga.input = ga._ragged_pad_to_longest(ga.input)")
	print("suggestion\t: truncate to shortest array")
	print("if yes, try\t: ga.input = ga._ragged_truncate_to_shortest(ga.input)")
	return True

def check_input_iterable(data):
	if not hasattr(data[0], "__iter__"):
		return warn_input_1D(data)
	
	if len(data) > 2:
		return warn_input_more_than_2D(data)
	
	m = len(data)
	n = len(data[0])

	if m >= n:
		return warn_input_shape(data)
	
	if 

	length = len(data[0][0])

	if any(length!=len(array) for array in data[0]):
		return warn_input_ragged_input_matrix()
	if any(length!=len(array) for array in data[1]):
		return warn_input_ragged_output_matrix()
	
def check_input_string(data):
	return False
	
def check_input(data):	# True is warning, False is no warning
	if data is None:
		print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program got empty input")
		return True
	elif isinstance(data, str):
		return check_input_string(data)
	elif hasattr(data, "__iter__"):
		return check_input_iterable(data)
	else:
		print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program currently supports only array input")
		return True
