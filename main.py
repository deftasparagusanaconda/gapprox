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

#def console_clear_line():
#	print("\033[1A\033[K\r", end='')

console_clear()

# import -----------------------------------------------------------------------

print()
print("importing argparse")
import argparse
print("importing numpy")
import numpy
#print(", getch", end='')
#from getch import getch, getche
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

# enums ------------------------------------------------------------------------

print("defining enums")
from enum import Enum

class InputGraphTypes(Enum):
	VALUES = 1
	POINTS = 2
	STRING = 3

class OutputGraphTypes(Enum):
	VALUES = 1
	POINTS = 2
	STRING = 3

# variables --------------------------------------------------------------------

print("initializing variables")

input_graph_type = None
input_graph = None
func_interp = None
func_approx = None
func_expr = None
func_iter_err_min_alg = None
func_stepper = None
func_error = None
output_graph_type = None

choice = None

# argparse ---------------------------------------------------------------------

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
	if input_graph_type is not None:
		print("[1] - input graph type\t\t\t\t=", InputGraphTypes(int(input_graph_type)).name.lower())
	else:
		print("[1] - input graph type\t\t\t\t=", input_graph_type)
	print("[2] - input graph\t\t\t\t=", str(input_graph)[:30])
	print("[3] - interpolation method\t\t\t=", func_interp)
	print("[4] - approximation method\t\t\t=", func_approx)
	print("[5] - expression function\t\t\t=", func_expr)
	print("[6] - iterative error minimization algorithm\t=", func_iter_err_min_alg)
	print("[7] - error function\t\t\t\t=", func_error)
	print("[8] - stepper function\t\t\t\t=", func_stepper)

	if output_graph_type is not None:
		print("[9] - output graph type\t\t\t\t=", OutputGraphTypes(int(output_graph_type)).name.lower())
	else:
                print("[9] - output graph type\t\t\t\t=", output_graph_type)

	print()
	print("[Enter] - start")
	print("[q]     - exit")
	print()

	match input("choice: "):
		case '1':
			input_graph_type = main_screen.get_input_graph_type(input_graph_type, InputGraphTypes)
		case '2':
			input_graph = main_screen.get_input_graph(input_graph, input_graph_type, InputGraphTypes)
		case '3':
			func_interp = main_screen.get_func_interp(func_interp)
		case '4':
			func_approx = main_screen.get_func_approx(func_approx)
		case '5':
			func_expr = main_screen.get_func_expr(func_expr)
		case '6':
			func_iter_err_min_alg = main_screen.get_func_iter_err_min_alg(func_iter_err_min_alg)
		case '7':
			func_error = main_screen.get_func_error(func_error)
		case '8':
			func_stepper = main_screen.get_func_stepper(func_stepper)
		case '9':
			output_graph_type = main_screen.get_output_graph_type(output_graph_type, OutputGraphTypes)
		case '\n':	# equivalent to just pressing [Enter]
			input("hmm? you pressed enter!")
		case 'q':
			break
		case 'exit':
			break
		case _:
			input("\nhmm... i dont think thats a valid choice...")

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
