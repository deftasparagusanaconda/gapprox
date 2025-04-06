# each parameterizer naturally links to a mathematical expression
# this is a registry for those links

from . import paramizer as _paramizer
from . import expression as _expression

paramizer_links = {
	_paramizer.dft: _expression.fourier_series
	_paramizer.dct: _expression.idct
	_paramizer.dst: _expression.idst
