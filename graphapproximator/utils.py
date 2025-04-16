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
