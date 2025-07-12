from importlib import import_module

__all__ = []

for name in ["core", "dag", "regressor", "types"]:
    try:
        mod = import_module(f"gapprox.{name}")
        globals()[name] = mod
        __all__.append(name)
    except ImportError:
        pass  # silently skip missing components

