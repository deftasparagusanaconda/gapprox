import dataclasses
import interpolate, approximate, expression, error, stepper

@dataclasses.dataclass
class Components:
	InputGraphTypes = ("values", "points", "string")
	OutputGraphTypes = ("values", "points", "string")
	Interpolators = tuple(value for value in interpolate.__dict__.values() if callable(value))
	Approximators = tuple(value for value in approximate.__dict__.values() if callable(value))
	Expressions = tuple(value for value in expression.__dict__.values() if callable(value))
	Errors = tuple(value for value in error.__dict__.values() if callable(value))
	Steppers = tuple(value for value in stepper.__dict__.values() if callable(value))

@dataclasses.dataclass
class OptionsAdvanced:
	keep_regressive_errors = False
	# will be expanded later

@dataclasses.dataclass
class Options:
	OptionsAdvanced
	input_graph_type = None
	function_interpolate = None
	function_approximate = None
	function_expression = None
	function_iter_err_min_alg = None
	function_stepper = None
	function_error = None
	output_graph_type = None
