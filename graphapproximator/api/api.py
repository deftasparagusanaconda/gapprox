# the heart of the project
# when you do `import graphapproximator as ga`, ga is automatically replaced by an instance of API
# the instance manages your current configuration of generator, structgen, interpolator, ...
# the instance also exposes a list of available modules (generators, structgens, interpolators, ...)

#from . import utils
#from .check_input import check_input
from graphapproximator import paramgens, structgens
#from .. import outliers, plotters
#from ..regressor import Optimizer, strategies

# ga.generator = ga.generators.dct already works
# but i want ga.generator.<tab> to show dct's arguments
	# this can be done by setting __dir__
# and also to let ga.generator.dct_type = 3 to set the argument
	# this can be done by overriding __setattr__
# and also to let the approximator use the generator with those arguments
	# this can be done by a wrapper with a modified __call__

# youll also have to capture the `ga.generator = something` assignment to change the ComponentWrapper's component
# i think that has to be implemented *inside* API
	
class API():
	#_stateful_components:list[str] = ["interpolator", "paramgen", "structgen"]

#	_assume_first_one_input = staticmethod(utils.assume_first_one_input)
#	_assume_last_one_output = staticmethod(utils.assume_last_one_output)
#	_assume_x_array = staticmethod(utils.assume_x_array)
#	_transpose = staticmethod(utils.transpose)
	
	# expose modules through the class instance
	paramgens = paramgens
#	regressors = strategies
	structgens = structgens
#	outliers = outliers
#	plotters = plotters
	"""
	# store configuration
	def __init__(self):
		_warn:bool = True		# show warnings
		_multithread:bool = True	# use n threads for n outputs
		super().__setattr__("regressor", Regressor())	# because its checked by __setattr__
		super().__setattr__("interpolator", None)
		super().__setattr__("paramgen", None)
		super().__setattr__("structgen", None)

		self.input = None
		self.output = None
	"""	

	def __init__(self):
		super().__setattr__("_check_input", True)	# check input signature
		super().__setattr__("_multithread", True)	# use n threads for n outputs

		self.paramgen = None
		self.structgen = None
#		self.plotter = plotters.plotter2
		
		super().__setattr__("input", None)		# to bypass input check
		self.output = None
	
	reset = __init__	# ga.reset() now resets the instance
	
#	def __setattr__(self, name, value):
		#if name in self._stateful_components:
		#	if value is not None:
		#		name = StatefulFunction(value)
		#	else:
		#		name = None
#		if name == "regressor":
#			super().__setattr("regressor.strategy", value)

#		elif name == "input" and self._check_input:
#			super().__setattr__(name, value)
#			if check_input(self.input):
#				print(f"disable check\t: ga._check_input = False")

#		else:
#			super().__setattr__(name, value)
	
	#def __getattr__(self, name):
	#	print("__getattr__", self, name)

#	def __getattr__(self, name):
#		if name in self._params:
#			return self._params[name]
#		raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
		
#	def __dir__(self):
#		

	# THE PIPELINE!!!! -----------------------------------------------------
	
	# input=None is kept for convenience-sake because
	# ga.approximate(something) is easier than
	# ga.input = something; ga.approximate()
	def approximate(self, input=None):
		"""calculate an approximation with the configuration given"""
		if input is not None:
			self.input = input
		temp = self.input

		if self.paramgen:
			temp = self.paramgen(temp)
		#if self.regressor.strategy:
		#	temp = self.regressor(self, temp, self.input, self.structgen)
		if self.structgen:	# params to any
			temp = self.structgen(temp)
		self.output = temp

		return temp

	# the end ~w~ ----------------------------------------------------------

	__call__ = approximate	# ga() and ga.approximate() are now same
	
	# provided for convenience, so you can do ga.line(something)
	@staticmethod
	def line(input, output_type="string"):
		"""least squares line approximation (https://en.wikipedia.org/wiki/Linear_least_squares)
provided for convenience"""
		return structgens.polynomial(paramgens.line.linear_regression(input), number_of_points=len(input), output_type=output_type)
	
#	def plot(self):
#		plotters.plotter2(self.input, self.output)

	def show(self):
		"""print current configuration"""
		print("input =", self.input)
		print("paramgen =", self.paramgen)
		#print("regressor =", self.regressor.strategy)
		print("structgen =", self.structgen)
		print("plotter =", self.plotter)
		print("output =", self.output)
	
	#def show_full(self):
	#	"""print current configuration + ALL sub-configurations"""
	#	self.show()
	#	print()
	#	print("regressor:")
	#	self.regressor.show_full()
	
	# basically what you see when you do `print(ga)` in the python interpreter
	def __repr__(self):
		return f"<API instance & module 'graphapproximator' at {hex(id(self))}>"
		
	def new(self):			# foo = ga.new() creates new instance
		"""return a new API instance"""
		return type(self)()
	
	def copy(self):			# foo = ga.copy() creates a copy
		"""returns a copy of the API instance"""
		from copy import deepcopy
		return deepcopy(self)

# ideally, API should not have any static methods
