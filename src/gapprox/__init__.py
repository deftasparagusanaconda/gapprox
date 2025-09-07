'python toolkit to approximate the function of a graph'

from . import paramgens, structgens
from . import outliers, plotters
from . import operator_dicts, constant_dicts
from .parser import parser
from .sampler import sampler
from .approximation.approximation import Approximation
from .expression import Expression
#from .dag import Dag
#from .edge import Edge
#from .node import Node
from .dag import Dag
#from .function import Function
#from .variable import Variable, variables
#from .constant import Constant, constants
#from .add_ast_to_dag import AddAstToDag

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: ['Approximation', 'Function', 'Expression', 'Constant', 'Variable', 'Dag', 'Edge', 'Node', 'paramgens', 'structgens', 'outliers', 'plotters', 'operator_dicts', 'constant_dicts', 'constants', 'variables']
