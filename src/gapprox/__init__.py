"python toolkit to approximate the function of a graph"

from . import paramgens, structgens
#from . import optimizer
from . import outliers, plotters
from .parser import parser
from .sampler import sampler
from .approximation.approximation import Approximation
from .expression.expression import Node, Edge, Dag, Expression
from .expression import functions
from .types.number_types.natural import Natural
from .types.number_types.whole import Whole
from .types.truth_types import *

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: ['Approximation', 'Expression', 'paramgens', 'structgens', 'parser', 'sampler', 'outliers', 'plotters', 'functions']
