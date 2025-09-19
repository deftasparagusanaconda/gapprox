'python toolkit to approximate the function of a graph'

__version__ = "0.3.2"

# enable data structure integrity checks and strict edge-case-raises, and other stuff
debug: bool = True	# should be False for release versions, but ill probably forget to set it lol

#from . import paramgens, structgens
#from . import outliers, plotters
from .operator_dict import operator_dict
from . import operators
from .parser import parser
from .sampler import sampler
#from .approximation.approximation import Approximation
from .dag import Node, Edge, Dag
from . import errors
from . import rewarders
from . import collapsers
from . import objectives
from .expression import Expression
#from . import visitors
from . import constants
from .symbol import Variable, Parameter, Constant#, make_variables, make_parameters, make_constants
from .ast_to_dag_visitor import AstToDagVisitor
from . import misc
from .misc import str_to_ast

# to denote the absence of something, instead of using None
_NULL = misc.Null()

# special payload to mark that a Node is an output node
OUTPUT_NODE_MARKER = misc.OutputNodeMarker()

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: [
		# module attributes
		 'debug'
		,'_NULL'
		,'OUTPUT_NODE_MARKER'

		# classes
		#,'Approximation'
		,'Expression'
		#,'Variable'
		#,'Parameter'
		#,'Constant'
		,'Node'
		,'Edge'
		,'Dag'
		,'AstToDagVisitor'

		# collections
		,'paramgens'
		,'structgens'
		,'outliers'
		,'plotters'
		,'errors'
		,'collapsers'
		,'rewarders'
		,'objectives'
		#,'visitors'
		#,'constants'
		#,'operators'
		,'misc'

		# dict
		,'operators_dict'

		# functions
		,'str_to_ast'
]

