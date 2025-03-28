# my sanity is going downhill
# i want to die

# high-schooler-friendly interactive hybrid TUI/GUI

# at any given time, the program only holds one values[]

# ----------
# section where program tries to launch its own terminal if one isnt available
# ----------

print("clearing console")

def console_clear():
	print("\033[2J\033[H", end='')

def console_clear_line():
	print("\033[1A\033[K\r", end='')

# import -----------------------------------------------------------------------

print("importing argparse")
import argparse
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
print("importing main_screen")
import main_screen

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

input_graph_type = None
input_graph = None
function_interpolate = None
function_approximate = None
function_expression = None
function_iter_err_min_alg = None
function_stepper = None
function_error = None
output_graph_type = None

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
	print("[0] - input graph type\t\t\t\t=", input_graph_type)
	print("[1] - input graph\t\t\t\t=", str(input_graph)[:30])
	if function_interpolate is None:
		print("[2] - interpolation method\t\t\t=", function_interpolate)
	else:
		print("[2] - interpolation method\t\t\t=", function_interpolate.__name__)
	
	if function_approximate is None:
		print("[3] - approximation method\t\t\t=", function_approximate)
	else:
		print("[3] - approximation method\t\t\t=", function_approximate.__name__)
	
	if function_expression is None:
		print("[4] - expression function\t\t\t=", function_expression)
	else:
		print("[4] - expression function\t\t\t=", function_expression.__name__)
	
	print("[5] - iterative error minimization algorithm\t=", function_iter_err_min_alg)

	if function_error is None:
		print("[6] - error function\t\t\t\t=", function_error)
	else:
		print("[6] - error function\t\t\t\t=", function_error.__name__)
	
	if function_stepper is None:
		print("[7] - stepper function\t\t\t\t=", function_stepper)
	else:
		print("[7] - stepper function\t\t\t\t=", function_stepper.__name__)
	
	print("[8] - output graph type\t\t\t\t=", output_graph_type)
	print()
	print("[Enter] - start")
	print("[q]     - exit")
	print()

	match input("choice: "):
		case '0':
			input_graph_type = main_screen.get_input_graph_type(input_graph_type, InputGraphTypes)
		case '1':
			input_graph = main_screen.get_input_graph(input_graph, input_graph_type, InputGraphTypes)
		case '2':
			function_interpolate = main_screen.get_function_interpolate(function_interpolate, Interpolators)
		case '3':
			function_approximate = main_screen.get_function_approximate(function_approximate, Approximators)
		case '4':
			function_expression = main_screen.get_function_expression(function_expression, Expressions)
		case '5':
			function_iter_err_min_alg = main_screen.get_function_iter_err_min_alg(function_iter_err_min_alg)
		case '6':
			function_error = main_screen.get_function_error(function_error, Errors)
		case '7':
			function_stepper = main_screen.get_function_stepper(function_stepper, Steppers)
		case '8':
			output_graph_type = main_screen.get_output_graph_type(output_graph_type, OutputGraphTypes)
		case '':	# equivalent to just pressing [Enter]
			input("hmm? you pressed enter!")
		case 'q':
			break
		case 'exit':
			break
		case choice:	# default case
			console_clear_line()
			console_clear_line()
			input(f"\nhmmm... i dont think {choice} is valid...")

print()
print("exiting program...")

#if args.no_tui is False:
#	import textual.app

# i have a lot of performance and multithreading ideas but they will be implemented later. get it working first, performance later
# first CLI, then TUI, then GUI
# 4 modes of operation: CLI, CLI+GUI, TUI, TUI+GUI (default)

# to-do: change enums to dynamically use the module's function names
# (also sort alphanumerically)

# func_approximation should have a "[1] - all" option

# how to handle overlapping y-values for same x-value?
