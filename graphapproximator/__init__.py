# no other copies of the version number should be stored. this is the *only* one
__version__ = "0.2.0"

from . import paramgens, structgens
from . import regressor
from . import outliers, plotters
from .parser import parser
from .sampler import sampler

from .api import API as _API
api = _API()
