class Colours:
	"""https://en.wikipedia.org/wiki/ANSI_escape_code#Select_Graphic_Rendition_parameters"""

	RESET 		= '\033[0m'
	BOLD		= '\033[1m'
	FAINT		= '\033[2m'
	ITALIC		= '\033[3m'
	UNDERLINE 	= '\033[4m'
	BLACK 		= '\033[30m'
	RED		= '\033[31m'	
	GREEN		= '\033[32m'
	YELLOW		= '\033[33m'
	BLUE		= '\033[34m'
	MAGENTA		= '\033[35m'
	CYAN		= '\033[36m'
	WHITE		= '\033[37m'
	BRIGHT_BLACK	= '\033[90m'
	BRIGHT_RED	= '\033[91m'
	BRIGHT_GREEN	= '\033[92m'
	BRIGHT_YELLOW	= '\033[93m'
	BRIGHT_BLUE	= '\033[94m'
	BRIGHT_MAGENTA	= '\033[95m'
	BRIGHT_CYAN	= '\033[96m'
	BRIGHT_WHITE	= '\033[97m'

def warn_input_dimensions(data, SUGGESTION_DIMENSION_MAX=3):
	"""warns if the input is likely a list of coordinate pairs, e.g., [(x1, y1), (x2, y2), ...]
the expected format is an array of value arrays: ([x1, x2, ...], [y1, y2, ...], ...)
recommends transpose() if the number of rows >= the number of columns"""

	if not data or not hasattr(data, "__iter__"):
		return
	if not data[0] or not hasattr(data[0], "__iter__"):
		return

	m = len(data)
	n = len(data[0])

	if m < n:
		return
		
	def short_repr(row):
		if len(row) == 1:
			return f"[{row[0]}]"
		elif len(row) <= SUGGESTION_DIMENSION_MAX:
			return f"[{', '.join(map(str, row))}]"
		else:
			return f"[{', '.join(map(str, row[:SUGGESTION_DIMENSION_MAX]))}, ...]"

	
	print(f"{Colours.BRIGHT_RED}input warning{Colours.RESET}\t: program takes ([x1,x2,x3,...], [y1,y2,y3,...], ...)")
	try:
		# current (wrong) input preview
		input_preview = [short_repr(row) for row in data[:SUGGESTION_DIMENSION_MAX]]
		if len(data) > SUGGESTION_DIMENSION_MAX:
			input_preview.append("...")
		print(f"current input\t: [{', '.join(input_preview)}]")

	except Exception:
		print(f"current input\t: (couldnt print input, sorry...)")
	
	try:
		transposed = list(zip(*data))
		pieces = [short_repr(row) for row in transposed]

		if len(pieces) > SUGGESTION_DIMENSION_MAX:
			suggestion = f"({', '.join(pieces[:SUGGESTION_DIMENSION_MAX])}, ...)"
		else:
			suggestion = f"({', '.join(pieces)})"

		print(f"did you mean\t: {suggestion}")
	except Exception:
		print(f"did you mean\t: (couldnt auto-suggest fix, sowwyy)")

	print(f"if yes, try\t: ga.input = ga.transpose(ga.input)")
	print(f"disable check\t: ga._warn_input_dimensions = False")
	print()

def transpose(matrix):
	m = len(matrix)
	n = len(matrix[0])

	output = [[None] * m for _ in range(n)]

	for i in range(m):
		for j in range(n):
			output[j][i] = matrix[i][j]

	return output

# converts a function to an object that can hold its arguments
class StatefulFunction:
	_update_params_when_called_with_params:bool = True
	
	# perhaps add init with arguments feature in the future?
	def __init__(self, function):
		from inspect import signature, _empty

		#self._params = {}
		super().__setattr__('_params', {})	# because _params is checked in __setattr__
		self._function = function
		self._signature = signature(self._function)
		
		for name, param in self._signature.parameters.items():
			self._params[name] = _empty if param.default is _empty else param.default
		
	def __call__(self, *args, **kwargs):
		from inspect import _empty
		bound = self._signature.bind_partial(*args, **kwargs)
		bound.apply_defaults()
		if self._update_params_when_called_with_params:
			self._params.update(bound.arguments)

		purged = {k:v for k,v in self._params.items() if v is not _empty}
		return self._function(**purged)
	
	def __dir__(self):
		return list(self._params.keys()) + list(self.__dict__.keys())
	
	def __setattr__(self, name, value):
		if name in self._params:
			self._params[name] = value
		else:
			super().__setattr__(name, value)
	
	def __getattr__(self, name):
		if name in self._params:
			return self._params[name]
		raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
	
	def __repr__(self):
		return f"<StatefulFunction at {hex(id(self))} for {self._function}, with params {self._params}>"
