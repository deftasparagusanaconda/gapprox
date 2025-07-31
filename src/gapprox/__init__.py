'python toolkit to approximate the function of a graph'

from . import paramgens, structgens
#from . import optimizer
from . import outliers, plotters
from .parser import parser
from .sampler import sampler
from .approximation.approximation import Approximation
from .expression.node import Node
from .expression.edge import Edge
from .expression.dag import Dag
from .expression.expression import Expression
from .expression import operator_dicts
from .expression import constant_dicts 

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: ['Approximation', 'Expression', 'paramgens', 'structgens', 'outliers', 'plotters', 'operator_dicts', 'constant_dicts']
