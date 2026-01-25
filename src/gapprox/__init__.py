'python toolkit to approximate the function of a graph'

__version__ = "0.6.0"

# enable data structure integrity checks and strict edge-case-raises, and other stuff
debug: bool = True	# should be False for release versions, but ill probably forget to set it lol

#from . import paramgens, structgens
#from . import outliers, plotters
from .default_context import default_context
from . import operators
#from .parser import parser
from .sampler import sampler
#from .approximation.approximation import Approximation
from .graph import Node, Edge, MultiDAG
from . import errors
from . import rewarders
from . import collapsers
from . import objectives
from . import domains
from .expression import Expression
#from .symbol import Variable, Parameter, Constant#, make_variables, make_parameters, make_constants
from .ast_to_multidag_visitor import AstToMultiDAGVisitor
from . import misc
from . import visitors
from .relations import OrderedExpression, Domain, Mapping, Relation, Function
from .optimizer import Optimizer, ParameterOptimizer, StructureOptimizer
from .decorators import input_metadata, output_metadata
from .objective import Objective
#from .misc import str_to_ast

# to denote the absence of something, instead of using None
#_NULL = misc.Null()

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: [
		# module attributes
		 'debug'
		,'_NULL'
		,'OUTPUT_NODE_MARKER'

		# classes
		,'AstToMultiDAGVisitor'
		#,'Approximation'
		#,'Variable'
		#,'Parameter'
		#,'Constant'
		,'Node'
		,'Edge'
		,'MultiDAG'
		,'Expression'
		,'OrderedExpression'
		,'Domain'
		,'Mapping'
		,'Relation'
		,'Function'
		,'Objective'
		,'Optimizer'
		,'ParameterOptimizer'

		# decorators
		,'input_metadata'
		,'output_metadata'

		# collections
		,'domains'
		,'paramgens'
		,'structgens'
		,'outliers'
		,'plotters'
		,'errors'
		,'collapsers'
		,'rewarders'
		,'objectives'
		,'visitors'
		#,'constants'
		,'operators'
		,'misc'

		# dict
		,'default_context'

		# functions
		#,'str_to_ast'
]

