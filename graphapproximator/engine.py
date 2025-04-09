# export line and parabola approximators into an external LUT

from dataclasses import dataclass
from .components import interpolators, parameterizers, expressions, error_metrics, predictors
from .components import anomaly_metrics, parser
from . import utils

@dataclass
class Engine(): 
	parameterizers = parameterizers
	expressions = expressions
	output_types = ("values", "points", "string")
	
	input = None
	output = None
	parameters = None

#	parameterizer = staticmethod(parameterizers.line.least_squares)
#	expression = staticmethod(expressions.polynomial.polynomial)
#	output_type = "string"
	parameterizer = None
	expression = None
	output_type = None
	# change to "output_type = str" soon
	
	#def auto():
		# mini-AI to choose which approximation is best

	# ga.approximate() updates ga.output
	# ga.approximate([1,2,3]) does not update ga.output
	def approximate(self, input=None):
		if input is None:
			if self.input is None:
				raise ValueError("no input provided")
			input = self.input
			is_volatile = True
		else:
			is_volatile = False

		if self.parameterizer is None:
			params = input
		else:
			params = self.parameterizer(input)

		if self.expression is None:
			output = params
		else:
			output = self.expression(params)
			
		if is_volatile:
			self.output = output
			
		return output
	
	def line(self, input):
		"""least squares line approximation (https://en.wikipedia.org/wiki/Linear_least_squares)"""
		return expressions.polynomial.polynomial(parameterizers.line.least_squares(input), number_of_points=len(input), output_type=self.output_type)
	linear = line
	
	#def parabola(self, input=None):
	#	"""parabola approximation"""
	#quad = quadratic = parabola
	
	def show(self):
		from matplotlib.pyplot import plot, show
		try:
			plot(self.input)
		except:
			pass
		try:
			plot(self.output)
		except:
			pass
		show()
	
	__call__ = approximate	# result = ga([1,2,3]) runs approximation
		
	def __repr__(self):
		return f"<module & class instance 'graphapproximator' at {hex(id(self))}>"
		
	def new(self, **kwargs):	# foo = ga.new() creates new instance
		"""returns a new instance of graphapproximator"""
		return type(self)(**kwargs)
	
	def copy(self):
		"""returns a copy of the current graphapproximator"""
		from copy import deepcopy
		return deepcopy(self)
