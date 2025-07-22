"python toolkit to approximate the function of a graph"

from . import paramgens, structgens
#from . import optimizer
from . import outliers, plotters
from .parser import parser
from .sampler import sampler
from .approximation.approximation import Approximation
from .expression.expression import Node, Edge, Dag, Expression

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: ['Approximation', 'Expression', 'paramgens', 'structgens', 'parser', 'sampler', 'outliers', 'plotters']
