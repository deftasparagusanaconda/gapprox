# the heart of the project
# when you do `import graphapproximator as ga`, ga is automatically replaced by an instance of API
# the instance manages your current configuration of generator, expression, interpolator, ...
# the instance also exposes a list of available modules (generators, expressions, interpolators, ...)

from . import interpolators, generators, expressions, outliers, parser
from .optimizer.optimizer import Optimizer
from .optimizer import strategies

# ga.generator = ga.generators.dct already works
# but i want ga.generator.<tab> to show dct's arguments
	# this can be done by setting __dir__
# and also to let ga.generator.dct_type = 3 to set the argument
	# this can be done by overriding __setattr__
# and also to let the approximator use the generator with those arguments
	# this can be done by a wrapper with a modified __call__
"""
_wrapped_components = ("parser", "interpolator", "generator", "expressions")
class ComponentWrapper:
	def __init__(self):	# innit? hahahaha
		print("__init__", self)
		self.component = None
		self.arguments = {}

	def __dir__(self):
		print("__dir__", self)
		from inspect import getfullargspec
		if self.component is None:
			return []
		thing = getfullargspec(self.component)
		return thing.args()
#		from inspect import signature
#		if self.component is None:
#			return []
#		return list(signature(self.component).parameters.keys())
	
	def __setattr__(self, name, value):	# self.name = value
		print("__setattr__", self, name, value)
		#if the attribute theyre trying to set is one of the modules, then-
		if name in _wrapped_components:
			super().__setattr__(name, value)
		else:
			self.arguments[name] = value

#	def __call__(self, *args, **kwargs):
#		print("__call__", self, *args, **kwargs)
#		if self.component is None:
#			raise ValueError("no component assigned!")
#		kwargs = {**self.arguments, **kwargs}
#		return self.component(*args, **kwargs)

	def __call__(self, *args, **kwargs):
		print("__call__", self, *args, **kwargs)
		if self.component is None:
			return None
		return self.component(*args, **kwargs)

	def __repr__(self):
	#	print("__repr__")
	#	if self.component is None:
	#		return "<ComponentWrapper (unassigned)>"
		return f"<ComponentWrapper for {self.component.__name__}>"

# youll also have to capture the `ga.generator = something` assignment to change the ComponentWrapper's component
# i think that has to be implemented *inside* API
"""
class API():
	# expose modules through the class instance
	parser = parser.parser
	interpolators = interpolators
	generators = generators
	optimizers = strategies		# ga.optimizer = something only sets its strategy
	expressions = expressions
	outliers = outliers
	output_types = ["values", "points", "string"]
	
	# store configuration
	# instance variables
	def __init__(self):
		print("__init__", self)
		self.input = None
		self.input_type = None
		self.interpolator = None
		self.generator = None
		self.optimizer = Optimizer()	# start instance/module hybrid
		self.expression = None
		self.output = None
		self.output_type = None
	reset = __init__	# ga.reset() now resets the instance
	"""
	# override attribute assignments like ga.generator = something
	def __setattr__(self, name, value):
		print("__setattr__", self, name, value)
		obj = self.__dict__.get
		if name in _wrapped_components:
			obj = self.__dict__.get(name)
			if isinstance(obj, ComponentWrapper):
				obj.component = value
		else:
			super().__setattr__(name, value)
	"""
	#def auto():
	#	"""mini-AI to choose which approximation is best"""
	
	# THE PIPELINE!!!! -----------------------------------------------------
	def approximate(self, input=None):
		# input=None is kept for convenience-sake because
		# ga.approximate(something) is easier than
		# ga.input = something; ga.approximate()
		"""calculate an approximation using the configuration given (in other words, start the data pipeline)"""
		if input is not None:
			self.input = input
		temp = self.input
		
		temp = parser.parser(temp)	# string to func
		temp = self.interpolator(temp)	# points to points
		temp = self.generator(temp)	# points to params
		temp = self.optimizer(self, temp, self.input, self.expression)	# params to params
		temp = self.expression(temp)	# params to any
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
