'python toolkit to approximate the function of a graph'

debug: bool = True	# should be False for release versions, but ill probably forget to set it lol

from . import paramgens, structgens
from . import outliers, plotters
from . import operator_dicts, constant_dicts
from .parser import parser
from .sampler import sampler
from .approximation.approximation import Approximation
from .expression import Expression
from .dag import InputNode, FunctionNode, OutputNode, Edge, Dag
from . import errors
from . import rewarders
from . import reductions
from . import objectives
from .function import Function
from .traversers import NodeVisitor, NodeTransformer
#from .add_ast_to_dag import AddAstToDag

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: [
		'debug',
		'Approximation', 
		'Function', 
		'Expression', 
		'InputNode', 
		'FunctionNode', 
		'OutputNode', 
		'Edge', 
		'Dag', 
		'paramgens', 
		'structgens', 
		'outliers', 
		'plotters', 
		'operator_dicts', 
		'constant_dicts', 
		'errors', 
		'reductions', 
		'rewarders', 
		'objectives',
		'NodeVisitor',
		'NodeTransformer'
]
