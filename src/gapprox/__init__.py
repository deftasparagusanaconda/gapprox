'python toolkit to approximate the function of a graph'

__version__ = "0.3.0.5"

# enable data structure integrity checks and strict edge-case-raises, and other stuff
debug: bool = True	# should be False for release versions, but ill probably forget to set it lol

#from . import paramgens, structgens
#from . import outliers, plotters
from . import operator_dicts, constant_dicts
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
from .symbol import Variable, Parameter, Constant

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
		,'operator_dicts'
		,'errors'
		,'collapsers'
		,'rewarders'
		,'objectives'
		,'visitors'
		,'constants'
]

