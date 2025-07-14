#from gapprox import paramgens, structgens, plotters, sampler

class Approximation():
	#_stateful_components:list[str] = ["interpolator", "paramgen", "structgen"]

#	_assume_first_one_input = staticmethod(utils.assume_first_one_input)
#	_assume_last_one_output = staticmethod(utils.assume_last_one_output)
#	_assume_x_array = staticmethod(utils.assume_x_array)
#	_transpose = staticmethod(utils.transpose)

	# expose modules through the class instance
#	__version__ = __version__
#	paramgens = paramgens
#	regressors = strategies
#	structgens = structgens
#	outliers = outliers
#	sampler = sampler.sampler
#	plotters = plotters
	"""
	# store configuration
	def __init__(self):
		super().__setattr__("regressor", Regressor())	# because its checked by __setattr__
		super().__setattr__("interpolator", None)
	"""

	def __init__(self, *, input=None, paramgen=None, structgen=None):
#		_warn:bool = True		# show warnings
#		_multithread:bool = True	# use n threads for n outputs
		
		super().__setattr__("_check_input", True)	# check input signature
		super().__setattr__("_multithread", True)	# use n threads for n outputs
		self.paramgen = paramgen
		self.structgen = structgen
#		self.plotter = plotters.plotter2
		
#		super().__setattr__("input", input)		# to bypass input check
		self.input = input
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
	def evaluate(self, input=None):
		"""evaluate an approximation with the configuration given"""
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
	
#	__call__ = approximate	# ga() and ga.approximate() are now same
	
#	# provided for convenience, so you can do ga.line(something)
#	@staticmethod
#	def line(input, output_type="string"):
#		"""least squares line approximation (https://en.wikipedia.org/wiki/Linear_least_squares)
#provided for convenience"""
#		return structgens.polynomial(paramgens.line.linear_regression(input), number_of_points=len(input), output_type=output_type)
	
#	def plot(self):
#		self.plotter(self.input, self.output)

	
	def get_config(self):
		return {
			"input": self.input,
			"paramgen": self.paramgen,
			"structgen": self.structgen,
			"output": self.output,
			"_check_input": self._check_input,
			"_multithread": self._multithread
		}

	def from_config(self, config:dict):
		self.input = config["input"]
		self.paramgen = config["paramgen"]
		self.structgen = config["structgen"]
		self.output = config["output"]
		self._check_input = config.get("_check_input", self._check_input)
		self._multithread = config.get("_multithread", self._multithread)

	def summary(self):
		"""print current configuration"""
		for key, value in self.get_config().items():
			print(f"{key}\t= {value}")

	#def show_full(self):
	#	"""print current configuration + ALL sub-configurations"""
	#	self.show()
	#	print()
	#	print("regressor:")
	#	self.regressor.show_full()
	
	# basically what you see when you do `print(ga)` in the python interpreter
	#def __repr__(self):
	#	return f"<API instance & module 'gapproximator' at {hex(id(self))}>"
		
	#def new(self):			# foo = ga.new() creates new instance
	#	"""return a new API instance"""
	#	return type(self)()

#	def __str__(self):		# print(ga.output) and print(ga) are now same
#		return self.output

#	def copy(self):			# foo = ga.copy() creates a copy
#		"""returns a copy of the API instance"""
#		from copy import deepcopy
#		return deepcopy(self)
