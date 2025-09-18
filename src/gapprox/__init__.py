'python toolkit to approximate the function of a graph'

__version__ = "0.3.1"

# enable data structure integrity checks and strict edge-case-raises, and other stuff
debug: bool = True	# should be False for release versions, but ill probably forget to set it lol

#from . import paramgens, structgens
#from . import outliers, plotters
from .operators_dict import operators_dict
from . import operators
from .parser import parser
from .sampler import sampler
#from .approximation.approximation import Approximation
from .dag import InputNode, FunctionNode, OutputNode, Edge, Dag
from . import errors
from . import rewarders
from . import collapsers
from . import objectives
from .function import Function
from . import visitors
from . import constants
from .symbol import Variable, Parameter, Constant#, make_variables, make_parameters, make_constants

# to denote the absence of something, instead of using None
from .misc import Null as _Null
_NULL = _Null()

# monkeypatch the __dir__ to clean up the module's autocomplete
from sys import modules
modules[__name__].__dir__ = lambda: [
		# module attributes
		 'debug'

		# classes
		,'Approximation'
		,'Function'
		,'Expression'
		,'Variable'
		,'Parameter'
		,'Constant'
		,'InputNode'
		,'FunctionNode'
		,'OutputNode'
		,'Edge'
		,'Dag'

		# collections
		,'paramgens'
		,'structgens'
		,'outliers'
		,'plotters'
		,'errors'
		,'collapsers'
		,'rewarders'
		,'objectives'
		,'visitors'
		,'constants'
		,'operators'

		# dict
		,'operators_dict'
]

