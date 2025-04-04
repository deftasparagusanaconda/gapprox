# my sanity is going downhill
# i want to die

# high-schooler-friendly interactive hybrid TUI/GUI

# at any given time, the program only holds one values[]

# ----------
# section where program tries to launch its own terminal if one isnt available
# ----------

# import -----------------------------------------------------------------------

print("importing argparse")
import argparse
print("importing dataclasses")
import dataclasses
print("importing decode")
import decode
print("importing interpolate")
import interpolate
print("importing approximate")
import approximate
print("importing error")
import error
print("importing stepper")
import stepper
print("importing err_min_alg_iter")
import err_min_alg_iter
print("importing expression")
import expression
print("importing outlier")
import outlier
print("importing main_functions")
import main_functions
from main_functions import console_clear, console_clear_line

# dicts ------------------------------------------------------------------------

print("defining dicts")

InputGraphTypes = ("values", "points", "string")
OutputGraphTypes = ("values", "points", "string")
Interpolators = tuple(value for value in interpolate.__dict__.values() if callable(value))
Approximators = tuple(value for value in approximate.__dict__.values() if callable(value))
Expressions = tuple(value for value in expression.__dict__.values() if callable(value))
Errors = tuple(value for value in error.__dict__.values() if callable(value))
Steppers = tuple(value for value in stepper.__dict__.values() if callable(value))

# variables --------------------------------------------------------------------

print("initializing variables")

@dataclasses.dataclass
class OptionsContainer:
	input_graph_type = None
	input_graph = None
	function_interpolate = None
	function_approximate = None
	function_expression = None
	function_iter_err_min_alg = None
	function_stepper = None
	function_error = None
	output_graph_type = None
	output_graph = None
	
class AdvancedOptionsContainer:
	keep_regressive_errors = False

# argparse ---------------------------------------------------------------------

print("checking arguments")

parser = argparse.ArgumentParser(description="graph approximator")
parser.add_argument("--no-tui", action="store_true", help="disable terminal user interface")
parser.add_argument("--no-gui", action="store_true", help="disable graphical user interface")
args = parser.parse_args()

print()
if args.no_tui is False and args.no_gui is False:
	#print("Running in TUI/GUI mode")
	print("TUI/GUI not yet implemented")
	print("running in CLI mode\n")
elif args.no_tui is False and args.no_gui is True:
	#print("running in TUI mode")
	print("TUI not yet implemented")
	print("running in CLI mode\n")
elif args.no_tui is True and args.no_gui is False:
	#print("running in CLI/GUI mode")
	print("GUI not yet implemented")
	print("running in CLI mode\n")
elif args.no_tui is True and args.no_gui is True:
	print("running in CLI mode\n")

# menu -------------------------------------------------------------------------

print("starting menu...")
print()

while True:
	console_clear()

	print("graph approximator")
	print()
	print("    [0] - advanced options\t\t=", AdvancedOptionsContainer)

	if input_graph_type is None:
		print("\033[91m    [1] - input graph type\t\t=", input_graph_type, '\033[0m')
	else:
		print("    [1] - input graph type\t\t=", input_graph_type)
	
	if input_graph is None:
		print("\033[91m    [2] - input graph\t\t\t=", str(input_graph)[:30], '\033[0m')
	else:
		print("    [2] - input graph\t\t\t=", str(input_graph)[:30])
		
	if function_interpolate is None:
		print("    [3] - interpolation method\t\t=", function_interpolate)
	else:
		print("    [3] - interpolation method\t\t=", function_interpolate.__name__)
	
	if function_approximate is None:
		print("\033[91m    [4] - approximation method\t\t=", function_approximate, '\033[0m')
	else:
		print("    [4] - approximation method\t\t=", function_approximate.__name__)
	
	if function_expression is None:
		print("\033[91m    [5] - expression function\t\t=", function_expression, '\033[0m')
	else:
		print("    [5] - expression function\t\t=", function_expression.__name__)
	
	print("    [6] - error minimization algorithm\t=", function_iter_err_min_alg)

	if function_error is None:
		print("    [7] - error function\t\t=", function_error)
	else:
		print("    [7] - error function\t\t=", function_error.__name__)
	
	if function_stepper is None:
		print("    [8] - stepper function\t\t=", function_stepper)
	else:
		print("    [8] - stepper function\t\t=", function_stepper.__name__)
	
	if output_graph_type is None:
		print("\033[91m    [9] - output graph type\t\t=", output_graph_type, '\033[0m')
	else:
		print("    [9] - output graph type\t\t=", output_graph_type)
	print("   [10] - output graph\t\t\t=", output_graph)
	print()
	print("[enter] - start")
	print("    [q] - exit")
	print()
	
	match input("choice: "):
		case '0':
			advanced_options = main_functions.get_advanced_options(AdvancedOptionsContainer)
		case '1':
			input_graph_type = main_functions.get_input_graph_type(input_graph_type, InputGraphTypes)
		case '2':
			input_graph = main_functions.get_input_graph(input_graph, input_graph_type, InputGraphTypes)
		case '3':
			function_interpolate = main_functions.get_function_interpolate(function_interpolate, Interpolators)
		case '4':
			function_approximate = main_functions.get_function_approximate(function_approximate, Approximators)
		case '5':
			function_expression = main_functions.get_function_expression(function_expression, Expressions)
		case '6':
			function_iter_err_min_alg = main_functions.get_function_iter_err_min_alg(function_iter_err_min_alg)
		case '7':
			function_error = main_functions.get_function_error(function_error, Errors)
		case '8':
			function_stepper = main_functions.get_function_stepper(function_stepper, Steppers)
		case '9':
			output_graph_type = main_functions.get_output_graph_type(output_graph_type, OutputGraphTypes)
		case "10":
			output_graph = main_functions.output_graph(output_graph)
		case '' | "start" | "Start" | "enter" | "Enter":
			output_graph = main_functions.get_output_graph(OptionsContainer, AdvancedOptionsContainer)
		case 'q' | "exit" | "Exit" | "back" | "Back" | "quit" | "QUIT":
			break
		case choice:	# default case
			console_clear_line()
			console_clear_line()
			input(f"\nhmmm... i dont think \"{choice}\" is valid...")

print()
print("exiting program...")

#if args.no_tui is False:i
#	import textual.app

# i have a lot of performance and multithreading ideas but they will be implemented later. get it working first, performance later
# first CLI, then TUI, then GUI
# 4 modes of operation: CLI, CLI+GUI, TUI, TUI+GUI (default)

# to-do: change enums to dynamically use the module's function names
# (also sort alphanumerically)

# func_approximation should have a "[1] - all" option

# how to handle overlapping y-values for same x-value?
