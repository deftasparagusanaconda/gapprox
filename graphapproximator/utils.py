# converts a function to an object that can hold its arguments
from inspect import signature, _empty

class StatefulFunction:
	_update_params_when_called_with_params:bool = True
	
	# perhaps add init with arguments feature in the future?
	def __init__(self, function):

		#self._params = {}
		super().__setattr__('_params', {})	# because _params is checked in __setattr__
		self._function = function
		self._signature = signature(self._function)
		
		for name, param in self._signature.parameters.items():
			self._params[name] = _empty if param.default is _empty else param.default
		
	def __call__(self, *args, **kwargs):
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

"""
class FunctionWithState:
	def __init__(self, func):
		from inspect import signature, Parameter
		self._func = func
		self._sig = signature(func)
		self._params = {}

		# initialize default values
		for name, param in self._sig.parameters.items():
			if param.default is not Parameter.empty:
				self._params[name] = param.default
			else:
				# required arg; we leave it unset unless explicitly passed
				pass

	# make keyword args discoverable via tab
	def __dir__(self):
		return list(self._params.keys()) + list(self.__dict__.keys())

	def __getattr__(self, name):
		if name in self._params:
			return self._params[name]
		raise AttributeError(f"{name} not found")

	def __setattr__(self, name, value):
		if name in ['_func', '_sig', '_params']:
			super().__setattr__(name, value)
		elif name in self._params:
			self._params[name] = value
		else:
			super().__setattr__(name, value)

	def __call__(self, *args, **kwargs):
		# allow override
		all_args = {**self._params, **kwargs}
		return self._func(*args, **all_args)

	def __repr__(self):
		return f"<FunctionWithState at {hex(id(self))} for {self._func}, with params {self._params}>"
"""
