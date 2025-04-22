from utils import Colours

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

def short_repr_1D(data, dim=MAX_PRINTED_ARRAY_DIM):
	"""formats an array like: 1, 2, 3, ..."""
	if hasattr(data, "__iter__"):
		return ", ".join(map(str, data[:dim])) + (", ..." if len(data) > dim else "")
	else:
		return str(data)

def short_repr_2D(arrays, dim=MAX_PRINTED_ARRAY_DIM):
	"""formats an array of arrays like: [1, 2, 3, ...], [4, 5, 6, ...], [7, 8, 9, ...], ..."""
	if hasattr(arrays, "__iter__"):
		output = ", ".join(f"[{short_repr(row, dim)}]" for row in arrays[:dim])
		output += (", ..." if len(arrays) > dim else "")
		return output
	else:
		return arrays 

def warn_array_type_outliers(data, most_common_type, name):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: found type outliers in {name}[x]")
	print(f"expected type\t: {most_common_type}")
	for index, element in enumerate(data):
		if type(element) != most_common_type:
			print(f"type outlier\t: {name}[{index}] {type(data[index])}: {data[index]}")
	print(f"did you mean\t:")
	print(f"if yes, try\t: ga.input = ga._autotype(ga.input)")

def warn_array_iter_outliers(data, most_common_iter, name):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: found iter outliers in {name}[x]")
	print(f"expected iter\t: {most_common_iter}")
	for index, element in enumerate(data):
		if hasattr(element, "__iter__") != most_common_iter:
			print(f"type outlier\t: {name}[{index}] {type(data[index])}: {data[index]}")
	print(f"did you mean\t:")
	print(f"if yes, try\t: ga.input = ga._pad_zero_arrays(ga.input)")
	print(f"did you mean\t:")
	print(f"if yet, try\t: ga.input = ga._truncate_arrays(ga.input)")

def warn_input_1D(data):
	recommendation = range(min(MAX_PRINTED_ARRAY_DIM+1,len(data)))
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes at least two arrays")
	print(f"did you mean\t: [{short_repr(recommendation)}], [{short_repr(data)}]")
	print(f"if yes, try\t: ga.input = ga._assume_x_array(ga.input)")

def warn_input_more_than_2D(data):
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
"""
def warn_input_ragged_matrix(i,j,k):
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: found inconsistent array lengths")
	print("suggestion\t: pad with zeroes to longest array")
	print("if yes, try\t: ga.input = ga._ragged_pad_to_longest(ga.input)")
	print("suggestion\t: truncate to shortest array")
	print("if yes, try\t: ga.input = ga._ragged_truncate_to_shortest(ga.input)")
"""
"""
def check_input_homogeneity(data):
	from collections import Counter

	# assumes data is iterable
	# assumes data[0] is iterable
	# assumes data[1] is iterable
	# does not assume data[0][x] is iterable	# could be SIMO
	# does not assume data[1][x] is iterable	# could be MISO

	inputs, outputs = data

	# check if inputs is just one array
	input_iter_attr_list = [hasattr(element, "__iter__") for element in inputs]
	has_multiple_inputs = Counter(input_iter_attr_list).most_common(1)[0][0]

	# check if outputs is just one array

	# input check section
	input_lengths = [len(array) for array in inputs] if 

	# output check section
	
	# check intra-array type homogeneity
	# check inter-array type homogeneity
	# check inter-array length homogeneity

def check_input_double_matrix_homogeneity(data, max_shown_elements=3):
	# assumes data shape of ([1,2,3], [1,2,3]) ([1,2,3], [1,2,3])
	all_arrays = data[0] + data[1]
	array_lengths = [len(array) for array in all_arrays]

	# Initialize lists to track issues
	length_outliers = []
	type_outliers = {}j
	array_types = [type(array) for array in all_arrays]
	distinct_array_types = set(array_types)

	# Check for sample length consistency
	if len(set(array_lengths)) > 1:
		most_common_length = max(set(array_lengths), key=sample_lengths.count)
		for i, arr in enumerate(all_arrays):
			if len(arr) != most_common_length:
				length_outliers.append(i)

	# Check for type consistency within each array
	for i, arr in enumerate(all_arrays):
		types = [type(el) for el in arr]
		most_common_type = max(set(types), key=types.count)
		outlier_elements = [
			(j, el, type(el).__name__)
			for j, el in enumerate(arr)
			if not isinstance(el, most_common_type)
		]
		if outlier_elements:
			type_outliers[i] = {
				"expected_type": most_common_type.__name__,
				"outliers": outlier_elements
			}

	# Check for array type mismatch (e.g., lists vs tuples)
	if len(distinct_array_types) > 1:
		print("mismatched array types detected!")
		print(f"Found the following types: {', '.join(t.__name__ for t in distinct_array_types)}")

	# Report sample length issues
	if length_outliers:
		print("Some arrays have inconsistent sample lengths:")
		for i in length_outliers:
			arr = all_arrays[i]
			print(f"	Array {i} has a length of {len(arr)} (expected: {most_common_len})")
			preview = arr[:max_shown_elements]
			print(f"		Preview: {preview}{', ...' if len(arr) > max_shown_elements else ''}")

	# Report type inconsistency issues
	if type_outliers:
		print("Some arrays contain mixed types:")
		for i, issue in type_outliers.items():
			print(f"	In array {i}, expected type: {issue['expected_type']}")
			for j, el, el_type in issue["outliers"][:max_shown_elements]:
				print(f"		Element[{j}] = {el} (type: {el_type})")
			if len(issue["outliers"]) > max_shown_elements:
				print(f
"""

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
		warn_array_type_outliers(data, most_common_type, "data")
		warning_count += 1

	element_iter_counter = Counter(hasattr(element, "__iter__") for element in data)
	element_iter_most_common = element_iter_counter.most_common(1)[0][0]

	if len(element_iter_counter) > 1:
		# iterable/non-iterable outliers present
		warn_array_iter_outliers(data, most_common_iter, "data")
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
			# likely a list of points, like (x1,y1),(x2,y2),(x3,y3) instead of [x1,x2,x3],[y1,y2,y3]
			warn_input_shape(data)
			warning_count += 1
		
		if m > 2:
			warn_input_more_than_2D(data)
			warning_count += 1
	
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
