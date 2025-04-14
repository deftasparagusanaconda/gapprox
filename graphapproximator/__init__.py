from .api import api
from . import approximators, expressions, analyzers, interpolators, optimizer, outliers, parser

"""
# when you do "import graphapproximator", it imports this directory as a module
# this __init__.py file will convert that from a module to an instance of API
# graphapproximator then becomes an instance/module hybrid
# the instance exposes the modules using dot notation (e.g. ga.interpolators)

from . import api, approximators, expressions, extrapolators, generators, interpolators, optimizer, outliers, parser

# spawn the default instance
_instance = api.API()

# make the package itself behave like an instance of Engine
def __getattr__(name):
    return getattr(_instance, name)

def __setattr__(name, value):
    return setattr(_instance, name, value)

def __dir__():
    return dir(_instance)

# replace the module import with the instance
from sys import modules
modules[__name__] = _instance
"""
