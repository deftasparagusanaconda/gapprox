import importlib as _importlib
from pathlib import Path as _Path

# get path of this directory
_here = _Path(__file__).parent

# iterate through files/folders in this dir
for _path in _here.iterdir():
	# skip __init__.py and hidden files
	if _path.name.startswith("_") or _path.name.startswith("."):
		continue

	if _path.is_file() and _path.suffix == ".py":
		_module_name = _path.stem
	elif _path.is_dir() and (_path / "__init__.py").exists():
		_module_name = _path.name
	else:
		continue

	# dynamically import and attach the module
	_imported = _importlib.import_module(f".{_module_name}", package=__name__)
	globals()[_module_name] = _imported
