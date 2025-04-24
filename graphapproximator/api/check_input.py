from .utils import Colours

MAX_PRINTED_ARRAY_DIM = 3
MAX_PRINTED_ARRAY_DEPTH = 3

# recursive function. AI generated lmao
def short_repr(obj, dim=MAX_PRINTED_ARRAY_DIM, max_depth=MAX_PRINTED_ARRAY_DEPTH, _depth=0):
    """formats nested structures up to max_depth
at each level, shows up to dim elements
beyond max_depth, replaces deeper structures with '...'"""

    if _depth >= max_depth:
        return "..."

    if isinstance(obj, (str, bytes)):
        return repr(obj)

    if hasattr(obj, "__iter__"):
        try:
            items = list(obj)
        except Exception:
            return str(obj)
	
        parts = []
        for i, item in enumerate(items):
            if i >= dim:
                parts.append("...")
                break
            parts.append(short_repr(item, dim=dim, max_depth=max_depth, _depth=_depth + 1))

        return "[" + ", ".join(parts) + "]"
    else:
        return str(obj)

def warn_input_type_outliers(data, most_common_type):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: found type outliers in data[x]")
	print(f"expected type\t: {most_common_type}")
	for index, element in enumerate(data):
		if type(element) != most_common_type:
			print(f"type outlier\t: data[{index}] {type(data[index])}: {data[index]}")
	print(f"did you mean\t:")
	print(f"if yes, try\t: ga.input = ga._autotype(ga.input)")

def warn_input_iter_outliers(data, most_common_iter):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: found iter outliers in data[x]")
	print(f"expected iter\t: {most_common_iter}")
	for index, element in enumerate(data):
		if hasattr(element, "__iter__") != most_common_iter:
			print(f"type outlier\t: data[{index}] {type(data[index])}: {data[index]}")
	print(f"did you mean\t:")
	print(f"if yes, try\t: ga.input = ga._pad_zero_arrays(ga.input)")
	print(f"did you mean\t:")
	print(f"if yet, try\t: ga.input = ga._truncate_arrays(ga.input)")

def warn_input_1D(data):
	recommendation = range(min(MAX_PRINTED_ARRAY_DIM+1,len(data)))
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes at least two arrays")
	print(f"did you mean\t: [{short_repr(recommendation)}], [{short_repr(data)}]")
	print(f"if yes, try\t: ga.input = ga._assume_x_array(ga.input)")

def warn_input_more_than_2_arrays(data):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes (input arrays), (output arrays)")
	print(f"did you mean\t: {short_repr(data[0])}, ({short_repr(data[1:])[1:-1]})")
	print(f"if yes, try\t: ga.input = ga._assume_first_one_input(ga.input)")
	print(f"did you mean\t: ({short_repr(data[:-1])[1:-1]}), {short_repr(data[-1])}")
	print(f"if yes, try\t: ga.input = ga._assume_last_one_output(ga.input)")

def warn_input_shape(data):
	"""warns if the input is likely a list of coordinate pairs, e.g., (x1, y1), (x2, y2), (x3, y3), ...
the expected format is an array of value arrays: [x1, x2, x3, ...], [y1, y2, y3, ...], ...ee
recommends transpose() if the number of rows >= the number of columns"""
	transposed = list(zip(*data))

	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes at least [x1, x2, x3, ...], [y1, y2, y3, ...]")
	print(f"did you mean\t: {short_repr(transposed)[1:-1]}")
	print(f"if yes, try\t: ga.input = ga._transpose(ga.input)")

def check_input_iterable(data) -> int:
	"""check input by various tests to guarantee compatibility and to help user
warnings must show verbose warnings and suggest commands to fix the problems"""
	# data is already checked to be iterable

	warning_count = 0

	from collections import Counter
	
	element_type_counter = Counter(type(element) for element in data)
	element_type_most_common = element_type_counter.most_common(1)[0][0]

	if len(element_type_counter) > 1:
		# type outliers present
		warn_array_type_outliers(data, most_common_type)
		warning_count += 1

	element_iter_counter = Counter(hasattr(element, "__iter__") for element in data)
	element_iter_most_common = element_iter_counter.most_common(1)[0][0]

	if len(element_iter_counter) > 1:
		# iterable/non-iterable outliers present
		warn_array_iter_outliers(data, most_common_iter)
		warning_count += 1
	
	if not element_iter_most_common:
		# likely an array
		warn_input_1D(data)
		warning_count += 1
	else:
		# likely a matrix/tensor
		m = len(data)
		n_avg = sum(len(element) if hasattr(element, "__iter__") else 1 for element in data) / m
		
		if m >= n_avg:
			# likely a tall matrix (or a list of points) like:
			# (x1,y1)
			# (x2,y2)
			# (x3,y3)
			# (x4,y4)
			# (x5,y5)
			# ...
			warn_input_shape(data)
			warning_count += 1
		else:
			# likely a wide matrix. something like:
			# [x1,x2,x3,x4,x5,...]
			# [y1,y2,y3,y4,y5,...]
			# [z1,z2,z3,z4,z5,...]
			
			if m == 1:
				
			elif m > 2:
				# likely an array of arrays
				warn_input_more_than_2_arrays(data)
				warning_count += 1
			else:
				# likely a
			

			if not hasattr(data[0][0], "__iter__"):
				return False
			
			length = len(data[0][0])
			
			if any(length!=len(array) for array in data[0]):
				warn_input_ragged_input_matrix()
				warning_count += 1
			if any(length!=len(array) for array in data[1]):
				warn_input_ragged_output_matrix()
				warning_count += 1
			
			#element_len_counter = Counter(len(element) if hasattr(element, "__iter__") else 1 for element in data)
			#element_len_most_common = element
	return warning_count
	
def check_input(data):	# True is warning, False is no warning
	if data is None:
		print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program got empty input")
		return 1
	#elif isinstance(data, str):
		#return check_input_string(data)
		#haha not implemented yet
	elif hasattr(data, "__iter__"):
		return check_input_iterable(data)
	else:
		print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program currently supports only array input")
		return 1
