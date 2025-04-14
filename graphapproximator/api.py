# the heart of the project
# when you do `import graphapproximator as ga`, ga is automatically replaced by an instance of API
# the instance manages your current configuration of generator, expression, interpolator, ...
# the instance also exposes a list of available modules (generators, expressions, interpolators, ...)

from . import interpolators, generators, expressions, outliers, plotters
from .parser import parser 
from .sampler import sampler
from .optimizer.optimizer import Optimizer
from .optimizer import strategies

# allows arguments of components to be visible by dot notation
class ConfigurableFunction:
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
		return f"<ConfigurableFunction for {self._func.__name__}, with params {self._params}>"

class api():
	# expose modules through the class instance 
	interpolators = interpolators
	generators = generators
	optimizers = strategies		# ga.optimizer = something only sets its strategy
	expressions = expressions
	parser = parser
	sampler = sampler
	outliers = outliers
	plotters = plotters
	output_types = ["values", "points", "string"]
	
	# store configuration
	def __init__(self):
		self.input = None
		self.input_type = None
		self.interpolator = None
		self.generator = None
		self._optimizer = Optimizer()	# start instance/module hybrid
		self.expression = None
		self.output = None
		self.output_type = None
		self.outliers = None
	reset = __init__	# ga.reset() now resets the instance
	
	#def auto():
	#	"""mini-AI to choose which approximation is best"""
	
	def __setattr__(self, name, value):
		# auto-wrap for configurable components
		wrappable = ["generator", "interpolator", "parser", "expression"]
		if name in wrappable and callable(value):
			value = ConfigurableFunction(value)
		super().__setattr__(name, value)
	
	# expose optimizer instance normally
	@property
	def optimizer(self):
		return self._optimizer
	# intercept the ga.optimizer = ... assigner
	@optimizer.setter
	def optimizer(self, value):
		if callable(value):		
			self._optimizer.strategy = value
		elif value is None:
			self._optimizer.strategy = None
		else:
			raise ValueError("assign a callable strategy or None only")
	# ga.optimizer = something is now an alias for:
	# ga.optimizer.strategy = something
	
	# THE PIPELINE!!!! -----------------------------------------------------
	def approximate(self, input=None):
		# input=None is kept for convenience-sake because
		# ga.approximate(something) is easier than
		# ga.input = something; ga.approximate()
		"""calculate an approximation using the configuration given (in other words, start the data pipeline)"""
		if input is not None:
			self.input = input
		temp = self.input

		if self.parser:		# string to any
			temp = self.parser(temp)
		if self.interpolator:	# points to points
			temp = self.interpolator(temp)
		if self.generator:	# points to params
			temp = self.generator(temp)
		if self.optimizer.strategy:	# params to params
			temp = self.optimizer(self, temp, self.input, self.expression)
		if self.expression:	# params to any
			temp = self.expression(temp)
		self.output = temp
		return temp
	# the end ~w~ ----------------------------------------------------------

	__call__ = approximate	# ga() and ga.approximate() now do the same thing
	
	# provided for convenience, so you can do ga.line(something)
	@staticmethod
	def line(input, output_type="string"):
		"""least squares line approximation (https://en.wikipedia.org/wiki/Linear_least_squares)
provided for convenience"""
		return expressions.polynomial(generators.line.least_squares(input), number_of_points=len(input), output_type=output_type)
	
	# should this be static? or take array1 & array2?
	def plot(self):
		"""plot input and output using matplotlib"""
		from matplotlib.pyplot import plot as plt_plot
		try:
			plt_plot(self.input)
		except:
			# add debugging prints here
			pass
		from matplotlib.pyplot import show as plt_show
		try:
			plt_plot(self.output)
		except:
			# add debugging prints here
			pass
		plt_show()	
                
	def show(self):
		"""print current configuration"""
		print("input =", self.input)
		print("input_type =", self.input_type)
		print("interpolator =", self.interpolator)
		print("generator =", self.generator)
		print("optimizer =", self.optimizer.strategy)
		print("expression =", self.expression)
		print("output =", self.output)
		print("output_type =", self.output_type)
	
	def show_full(self):
		"""print current configuration + ALL sub-configurations"""
		self.show()
		print()
		print("optimizer:")
		self.optimizer.show_full()

	# basically what you see when you do `print(ga)` in the python interpreter
	def __repr__(self):
		return f"<API instance & module 'graphapproximator' at {hex(id(self))}>"
		
	def new(self):			# foo = ga.new() creates new instance
		"""return a new instance of Engine"""
		return type(self)()
	
	def copy(self):			# foo = ga.copy() creates a copy
		"""returns a copy of the current Engine instance"""
		from copy import deepcopy
		return deepcopy(self)

# ideally, API should not have any static methods
