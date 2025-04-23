from .interpolators import *
from . import line
from .zeroes import zeroes

"""
from importlib import import_module as _import_module
from pathlib import Path as _Path

_here = _Path(__file__).parent
for _path in _here.glob("*.py"):
	if _path.name.startswith("_"):
		continue	# skip private and dunder files like __init__.py
	
	_module_name = _path.stem	# filename without extension
	_module = _import_module(f".{_module_name}", package=__name__)
	globals()[_module_name] = _module
"""


"""
import pathlib

here = pathlib.Path()
files = here.glob(".py")
print(here)
print(files)

for file in files:
	if file.name.startswith("_"):	 # skip private and dunder files like __init__.py
		continue	 # skip private and dunder files like __init__.py
	
	module = file.stem
"""
