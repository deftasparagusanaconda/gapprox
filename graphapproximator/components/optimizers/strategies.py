# this module contains things specific to optimizer.py

class _SingleThread:
	def __call__(optimizer, input_params, input_actual, expression):	
		iter_limit = 100	# magic number, for testing for now...
		for _ in range(iter_limit):
			self.iterate(ga)
single_thread = _SingleThread()

class _CompetitionSerial:
	def __call__(optimizer, input_params, input_actual, expression):
		print("not made yet! lol")
competition_serial = _CompetitionSerial()

class _CompetitionParallel:
	#	census_modes = ["iter","time"]
	def __call__(optimizer, input_params, input_actual, expression):
		print("not made yet! come back later!")
	#	census_mode = "iter"
		# should competition_parallel call a census when a thread runs a number of iterations? or when all threads run a number of iterations? or when their average reaches that amount? or what?
competition_parallel = _CompetitionParallel()
