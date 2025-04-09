# start the GUI (or CLI)

import argparse
parser = argparse.ArgumentParser(description="graph approximator")
parser.add_argument("--headless", action="store_true", help="disable graphical user interface")
args = parser.parse_args()

import graphapproximator as ga	# importing automatically starts an engine

if args.headless:
	from cli.cli import cli
	cli(ga)
else:
	from gui.gui import gui
	gui(ga)

print()
print("exiting program...")
