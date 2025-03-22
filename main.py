# high-schooler-friendly interactive hybrid TUI/GUI

# at any given time, the program only holds one values[]

import argparse
parser = argparse.ArgumentParser(description="Graph Approximator CLI")
parser.add_argument("--headless", action="store_true", help="Run in terminal mode without a graphical interface")
args = parser.parse_args()

if args.headless is True:
	print("Running in headless (TUI) mode...")
else:
	print("Running in hybrid (TUI/GUI) mode...")

print()
print("importing interpolate.py")
import interpolate
print("importing approximate.py")
import approximate
print("importing error.py")
import error
print("importing step.py")
import step
print("importing err_min_alg_iter.py")
import err_min_alg_iter
print("importing expression.py")
import expression

import textual.app



# i have a lot of performance and multithreading ideas but they will be implemented later. get it working first, performance later
