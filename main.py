# high-schooler-friendly interactive hybrid TUI/GUI

# at any given time, the program only holds one values[]

# ----------
# section where program tries to launch its own terminal if one isnt available
# ----------

print("\033[2J\033[H", end='')	# clear console

import argparse
parser = argparse.ArgumentParser(description="graph approximator")
parser.add_argument("--no-tui", action="store_true", help="disable terminal user interface")
parser.add_argument("--no-gui", action="store_true", help="disable graphical user interface")
args = parser.parse_args()

if args.no_tui is False and args.no_gui is False:
#	print("Running in TUI/GUI mode...")
	print("TUI/GUI not yet implemented")
	print("running in CLI mode...\n")
elif args.no_tui is False and args.no_gui is True:
#	print("running in TUI mode...")
	print("TUI not yet implemented")
	print("running in CLI mode...\n")
elif args.no_tui is True and args.no_gui is False:
#	print("running in CLI/GUI mode...")
	print("GUI not yet implemented")
	print("running in CLI mode...\n")
elif args.no_tui is True and args.no_gui is True:
	print("running in CLI mode...\n")

print("importing numpy")
import numpy

print()
print("importing decoders")
import decode
print("importing interpolators")
import interpolate
print("importing approximators")
import approximate
print("importing error functions")
import error
print("importing step functions")
import step
print("importing error minimization algorithms")
import err_min_alg_iter
print("importing expressions")
import expression

from enum import Enum
class InputTypes(Enum):
	VALUES = 1
	POINTS = 2
	STRING = 3

class ErrMinAlgIterType(Enum):
	NONE = 0

print()
while True:
	print("input type [" + ", ".join(f"{type.value}-{type.name.lower()}" for type in InputTypes) + "]: ", end='')
	ingraph_type = int(input())
	if ingraph_type not in InputTypes:
		print("\033[1A\033[K\r", end='')	# clear line
		continue
	else:
		break

if ingraph_type is InputTypes.VALUES:
	ingraph_values = tuple(float(value) for value in input("input values: ").split(','))
func_approximate = input("approximation: ")
func_expression = input("expression: ")

#print()
#print("input type:", ingraph_type)
#print("input values: ", ingraph_values)

"""
func_err_min_alg_iter = input()
func_error = input()
func_step = input()
"""

"""
if args.no_tui is False:
	import textual.app
"""





# i have a lot of performance and multithreading ideas but they will be implemented later. get it working first, performance later
# first CLI, then TUI, then GUI
# 4 modes of operation: CLI, CLI+GUI, TUI, TUI+GUI (default)
