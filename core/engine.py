from dataclasses import dataclass
from . import interpolator, parameterizer, expression, error, stepper

@dataclass
class Engine: 
	input_types = ("values", "points", "string")
	output_types = ("values", "points", "string")
	interpolators = interpolator
	parameterizers = parameterizer
	expressions = expression
	errors = error
	steppers = stepper
	
	input = None
	input_type = None
	output = None
	output_type = None
	interpolator = None
	parameterizer = None
	expression = None
	stepper = None
	error = None
	
	@dataclass
	class _AdvancedOptions:
	        keep_regressive_errors = False
	        # will be expanded later
	advanced_options = _AdvancedOptions()

	def __repr__(self):
		return f"<module 'graphapproximator' (Engine instance) at {hex(id(self))}>"
	
	def copy(self):
		"""create a copy of the current graphapproximator"""
		from copy import deepcopy
		return deepcopy(self)

	def approximate(self, input=None):	# wrapper function for combining the components. just a demo, kinda
		if input == None:
			input = self.input
		params = self.parameterizer(input)
		self.output = self.expression(params)	# store result
		return self.output			# and also return result

	__call__ = approximate	# allows approx = ga([1,2,3]) to do an immediate approximation
