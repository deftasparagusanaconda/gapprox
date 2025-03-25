# high-schooler-friendly interactive hybrid TUI/GUI

# at any given time, the program only holds one values[]

# ----------
# section where program tries to launch its own terminal if one isnt available
# ----------

def console_clear():
	print("\033[2J\033[H", end='')

def console_clear_line():
	print("\033[1A\033[K\r", end='')

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
print("importing iter_err_min_alg")
import iter_err_min_alg
print("importing expression")
import expression
print("importing outlier")
import outlier

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

# menu screens -----------------------------------------------------------------

print("setting up menu screens")
def screen_menu():
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
	print("\nchoice: ", end='')

	return input()

def screen_input_graph_type():
	console_clear()

	while True:
		if input_graph_type is not None:
			print("input graph type =", InputGraphTypes(int(input_graph_type)).name.lower())
		else:
			print("input graph type =", input_graph_type)

		print()
		print("[0] - None")
		for inputgraphtype in InputGraphTypes:
			print(f"[{inputgraphtype.value}] - {inputgraphtype.name.lower()}")

		for i in range(10-len(InputGraphTypes)):
			print()
		
		print("[q] - exit")
		print()
		output = input("choice: ")
		
		if '0' == output:
			return None
		
		if 'q' == output:
			return input_graph_type
		
		if eval(output) not in InputGraphTypes:
			console_clear()
			continue
		else:
			break

	return output

def screen_input_graph():
	console_clear()

	if input_graph_type is None:
		print("set input graph type first")
		print()
		print("[Enter]")
		print()
		input("choice: ")
		return None

	if input_graph_type == InputGraphTypes.VALUES.value:
		output = input("input values (separated by ','): ")
		output = tuple(float(value) for value in output.split(','))	
	elif input_graph_type == InputGraphTypes.POINTS.value:
		output = input("input points: ")
		output = tuple(tuple(float(value) for coord in point) for point in output.split(')'))
	elif input_graph_type == InputGraphTypes.STRING.value:
		output = input("input string: ")
	else:
		output = None
	
	return output

def screen_func_interp():
	return input("interpolation method: ")

def screen_func_approx():
	return input("approximation method: ")

def screen_func_expr():
	return input("expression function: ")

def screen_func_iter_err_min_alg():
	return input("iterative error minimization algorithm: ")

def screen_func_error():
	return input("error function: ")

def screen_func_stepper():
	return input("stepper function: ")

def screen_output_graph_type():
	console_clear()

	while True:
		if output_graph_type is not None:
			print("output graph type =", OutputGraphTypes(int(output_graph_type)).name.lower())
		else:
			print("output graph type =", output_graph_type)

		print()
		print("[0] - None")
		for outputgraphtype in OutputGraphTypes:
			print(f"[{outputgraphtype.value}] - {outputgraphtype.name.lower()}")

		for i in range(10-len(OutputGraphTypes)):
			print()
		
		print("[q] - exit")
		print()
		output = input("choice: ")
		
		if '0' == output:
			return None
		
		if 'q' == output:
			return output_graph_type
		
		if eval(output) not in OutputGraphTypes:
			console_clear()
			continue
		else:
			break

	return output

def screen_input_graph():
	console_clear()

	if input_graph_type is None:
		print("set input graph type first")
		print()
		print("[Enter]")
		print()
		input("choice: ")
		return None

	if input_graph_type == InputGraphTypes.VALUES.value:
		output = input("input values (separated by ','): ")
		output = tuple(float(value) for value in output.split(','))	
	elif input_graph_type == InputGraphTypes.POINTS.value:
		output = input("input points: ")
		output = tuple(tuple(float(value) for coord in point) for point in output.split(')'))
	elif input_graph_type == InputGraphTypes.STRING.value:
		output = input("input string: ")
	else:
		output = None
	
	return output

def screen_func_interp():
	return input("interpolation method: ")

def screen_func_approx():
	return input("approximation method: ")

def screen_func_expr():
	return input("output graph type: ")

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

# menu -------------------------------------------------------------------------

print()
print("starting menu...")
print()

while True:
	match screen_menu():
		case '0':
			print("ass!!!")
		case '1':
			input_graph_type = screen_input_graph_type()
		case '2':
			input_graph = screen_input_graph()
		case '3':
			func_interp = screen_func_interp()
		case '4':
			func_approx = screen_func_approx()
		case '5':
			func_expr = screen_func_expr()
		case '6':
			func_iter_err_min_alg = screen_func_iter_err_min_alg()
		case '7':
			func_error = screen_func_error()
		case '8':
			func_stepper = screen_func_stepper()
		case '9':
			output_graph_type = screen_output_graph_type()
		case '\n':	# equivalent to just pressing [Enter]
			print("enter!")
#		break

		case 'q':
			break
		case 'exit':
			break

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
