# the heart of the project
# when you do `import graphapproximator as ga`, ga is automatically replaced by an instance of API
# the instance manages your current configuration of generator, structgen, interpolator, ...
# the instance also exposes a list of available modules (generators, structgens, interpolators, ...)

#from . import utils
#from .check_input import check_input
from hana import __version__, paramgens, structgens, plotters, sampler
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
	
class HelpMessage:
	help_message = """hana is a python toolkit for approximating the function of a graph
doing `import hana` makes hana an instance of API

commands:
    hana()                  run an approximation using the configuration
    hana.approximate()      same as hana()
    hana.show()             display your current configuration
    hana.reset()            "scratch that. start over.."
    ... = hana.new()        make a brand new session
    ... = hana.copy()       clone this session (like a checkpoint!)
						
configuration:
    hana.input = ...        what you give it
    hana.output = ...       what it gives you back
    hana.paramgen = ...     how we generate the parameters
    hana.structgen = ...    how we build the structure of the function
				
extras:
    hana.line(...)          do a quick line approximation
    hana.__version__        check the version youre using
    hana.help               (this help message)

for more, see https://github.com/deftasparagusanaconda/hana/"""

	def __str__(self):		# str(hana.help) or print(hana.help) or 
		return self.help_message
	def __call__(self):		# hana.help()
		print(self.help_message)
	def __repr__(self):		# hana.help
		return self.help_message

class API():
	#_stateful_components:list[str] = ["interpolator", "paramgen", "structgen"]

#	_assume_first_one_input = staticmethod(utils.assume_first_one_input)
#	_assume_last_one_output = staticmethod(utils.assume_last_one_output)
#	_assume_x_array = staticmethod(utils.assume_x_array)
#	_transpose = staticmethod(utils.transpose)

	help = HelpMessage()
	
	# expose modules through the class instance
	__version__ = __version__
	paramgens = paramgens
#	regressors = strategies
	structgens = structgens
#	outliers = outliers
	sampler = sampler
	plotters = plotters
	"""
	# store configuration
	def __init__(self):
		super().__setattr__("regressor", Regressor())	# because its checked by __setattr__
		super().__setattr__("interpolator", None)
	"""

	def __init__(self):
		_warn:bool = True		# show warnings
		_multithread:bool = True	# use n threads for n outputs
		
		super().__setattr__("_check_input", True)	# check input signature
		super().__setattr__("_multithread", True)	# use n threads for n outputs
		self.paramgen = None
		self.structgen = None
		self.plotter = plotters.plotter2
		
		super().__setattr__("input", None)		# to bypass input check
		self.output = None
	reset = __init__	# hana.reset() now resets the instance
	
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
#				print(f"disable check\t: hana._check_input = False")

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
	
#	@staticmethod
#	def help(self):
#		"""this function prints the docstring of graphapproximator.api, which also doubles as its help message
#if you see this, you probably did something wrong. perhaps try one of the following:
#ga.help, ga.help(), help(ga), print(ga.help), print(ga.help()), ga.__doc__, print(ga.__doc__)
#if the prompt shows "NameError: name 'ga' is not defined", try `import graphapproximator.api as ga` and try again
#otherwise, go to https://github.com/deftasparagusanaconda/graphapproximator"""
#		print(self.__doc__, end='')
#		return self.__doc__
	
	__call__ = approximate	# ga() and ga.approximate() are now same
	
	# provided for convenience, so you can do ga.line(something)
	@staticmethod
	def line(input, output_type="string"):
		"""find line of least squares (https://en.wikipedia.org/wiki/Linear_least_squares)"""
		return structgens.polynomial(paramgens.line.linear_regression(input), number_of_points=len(input), output_type=output_type)
	
	def plot(self):
		self.plotter(self.input, self.output)

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
	
	# basically what you see when you do print(hana) in the python interpreter
	def __repr__(self):
		return f"<API instance & module 'hana' at {hex(id(self))}>"
		
	def new(self):			# thing = hana.new() creates new instance
		"""return a new API instance"""
		return type(self)()
	
	def copy(self):			# thing = hana.copy() creates a copy
		"""returns a copy of the API instance"""
		from copy import deepcopy
		return deepcopy(self)
