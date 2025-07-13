class Colours:
	"""https://en.wikipedia.org/wiki/ANSI_escape_code#Select_Graphic_Rendition_parameters"""

	RESET          = '\033[0m'
	BOLD           = '\033[1m'
	FAINT          = '\033[2m'
	ITALIC         = '\033[3m'
	UNDERLINE      = '\033[4m'
	BLACK          = '\033[30m'
	RED            = '\033[31m'	
	GREEN          = '\033[32m'
	YELLOW         = '\033[33m'
	BLUE           = '\033[34m'
	MAGENTA        = '\033[35m'
	CYAN           = '\033[36m'
	WHITE          = '\033[37m'
	BRIGHT_BLACK   = '\033[90m'
	BRIGHT_RED     = '\033[91m'
	BRIGHT_GREEN   = '\033[92m'
	BRIGHT_YELLOW  = '\033[93m'
	BRIGHT_BLUE    = '\033[94m'
	BRIGHT_MAGENTA = '\033[95m'
	BRIGHT_CYAN    = '\033[96m'
	BRIGHT_WHITE   = '\033[97m'

MAX_PRINTED_ARRAY_DIM = 3

def most_common(array):
	from collections import Counter
	return Counter(array).most_common(1)[0][0]

def short_repr(row, dim=MAX_PRINTED_ARRAY_DIM):
	if len(row) <= dim:
		return ", ".join(map(str, row))
	return ", ".join(map(str, row[:dim])) + ", ..."

def short_array_repr(arrays, dim=MAX_PRINTED_ARRAY_DIM):
	"""formats list of arrays like: [1, 2, 3, ...], [4, 5, 6, ...], ..."""
	return ", ".join(
		f"[{short_repr(row, dim)}]" for row in arrays[:dim]
	) + (", ..." if len(arrays) > dim else "")

def assume_first_one_input(data):
	return (data[0], data[1:])

def assume_last_one_output(data):
	return (data[:-1], data[-1])

def assume_x_array(data):
	return (list(range(len(data))), data)

def transpose(matrix):
	m = len(matrix)
	n = len(matrix[0])

	output = [[None] * m for _ in range(n)]	# initialize memory

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
