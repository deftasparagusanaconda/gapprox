# this module contains things specific to regressor.py
"""
# one thread works iteratively
class _SingleThread:
	def __call__(optimizer, input_params, input_actual, expression):	
		iter_limit = 100	# magic number, for testing for now...
		for _ in range(iter_limit):
			self.iterate(ga)
single_thread = _SingleThread()

# multiple threads compute one iteration, then compare each other
class _CompetitionSerial:
	def __call__(optimizer, input_params, input_actual, expression):
		print("not made yet! lol")
competition_serial = _CompetitionSerial()

# multiple threads compute a few iterations, then compare each other
# a "census" is called to compare the threads
class _CompetitionParallel:
		#census_modes = ["iter","time"]
	def __call__(optimizer, input_params, input_actual, expression):
		print("not made yet! come back later!")
		#census_mode = "iter"
		# should competition_parallel call a census when a thread runs a number of iterations? or when all threads run a number of iterations? or when their average reaches that amount? or what?
competition_parallel = _CompetitionParallel()
"""

# one thread works iteratively
def single_thread(regressor, input_params, input_actual, expression):	
	iter_limit = 100	# magic number, for testing for now...
	for _ in range(iter_limit):
		self.iterate(ga)

# multiple threads compute one iteration, then compare each other
def competition_serial(regressor, input_params, input_actual, expression):
	print("not made yet! lol")

# multiple threads compute a few iterations, then compare each other
# a "census" is called to compare the threads
def competition_parallel(regressor, input_params, input_actual, expression):
	print("not made yet! come back later!")
	#census_modes = ["iter","time"]
	#census_mode = "iter"
	# should competition_parallel call a census when a thread runs a number of iterations? or when all threads run a number of iterations? or when their average reaches that amount? or what?
