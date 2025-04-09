# export line and parabola approximators into an external LUT

from dataclasses import dataclass
from .components import interpolators, generators, expressions, outliers, parser
from . import utils

@dataclass
class Engine():
	parser = parser.parser
	interpolators = interpolators
	generators = generators
	expressions = expressions
	outliers = outliers
	output_types = ("values", "points", "string")
	
	input = None
	output = None
	parameters = None
	interpolator = None
	generator = None
	expression = None
	input_type = None
	output_type = None
	outliers = None
	
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
	
		if self.generator is None:
			params = input
		else:
			params = self.generator(input)
	
		if self.expression is None:
			output = params
		else:
			output = self.expression(params)
			
		if is_volatile:
			self.output = output
			
		return output

	@staticmethod
	def line(input, output_type="string"):
		"""least squares line approximation (https://en.wikipedia.org/wiki/Linear_least_squares)"""
		return expressions.polynomial.polynomial(generators.line.least_squares(input), number_of_points=len(input), output_type=output_type)
	linear = line
	
	#@staticmethod
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
	plot = show
	
	__call__ = approximate	# ga([1,2,3]) runs approximation
		
	def __repr__(self):
		return f"<module & class instance 'graphapproximator' at {hex(id(self))}>"
		
#	def new(self, **kwargs):	# foo = ga.new() creates new instance
#		"""returns a new instance of graphapproximator"""
#		return type(self)(**kwargs)
	def new(self):			# foo = ga.new() creates new instance
		"""return a new instance of the graphapproximator engine"""
		return type(self)
	
	def copy(self):
		"""returns a copy of the current graphapproximator engine"""
		from copy import deepcopy
		return deepcopy(self)
